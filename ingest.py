"""Milestone 3 -- document ingestion and chunking.

Reads the cleaned .txt files in processed_data/, pulls out each document's
title, section headers, and Source URL, then splits the body into ~100-token
chunks with 20 tokens of overlap, cut on sentence and list-item boundaries
(see planning.md -> Chunking Strategy).

Each cleaned file is expected to look like:

    TITLE LINE IN CAPS

    SECTION HEADER
    body text...

    ANOTHER SECTION HEADER
    body text...

    Source: https://...

Run it:
    python ingest.py                 # writes chunks.json, prints stats + samples
    python ingest.py --preview 5     # show 5 full sample chunks for the README
    python ingest.py --chunk-size 500 --overlap 75
"""

import argparse
import json
import random
import re
from dataclasses import dataclass, field
from pathlib import Path

from chunking import (
    CHUNK_OVERLAP,
    CHUNK_SIZE,
    EMBEDDING_MODEL,
    chunk_text,
    count_tokens,
    get_tokenizer,
    is_section_header,
)

PROJECT_ROOT = Path(__file__).resolve().parent
INPUT_DIR = PROJECT_ROOT / "processed_data"
OUTPUT_FILE = PROJECT_ROOT / "chunks.json"

# all-MiniLM-L6-v2 truncates its input at this many tokens.
MODEL_MAX_TOKENS = 256

SOURCE_LINE = re.compile(r"^\s*Source\s*:\s*(\S.*)$", re.IGNORECASE)


@dataclass
class Document:
    doc_id: str
    title: str
    source_url: str
    source_file: str
    body: str
    # (start_char_in_body, header_text) for every section header found
    sections: list[tuple[int, str]] = field(default_factory=list)

    @property
    def token_count(self) -> int:
        return count_tokens(self.body)


def parse_document(path: Path) -> Document:
    """Parse one cleaned .txt file into a Document."""
    raw = path.read_text(encoding="utf-8")
    lines = raw.splitlines()

    title = ""
    source_url = ""
    body_lines: list[str] = []

    for i, line in enumerate(lines):
        match = SOURCE_LINE.match(line)
        if match:
            source_url = match.group(1).strip()
            continue
        if not title and line.strip():
            # First non-empty line is the document title.
            title = line.strip()
            continue
        body_lines.append(line)

    # Drop leading/trailing blank lines but keep interior structure.
    while body_lines and not body_lines[0].strip():
        body_lines.pop(0)
    while body_lines and not body_lines[-1].strip():
        body_lines.pop()

    body = "\n".join(body_lines)

    # Record where each section header starts, in body coordinates.
    sections: list[tuple[int, str]] = []
    offset = 0
    for line in body_lines:
        if is_section_header(line):
            sections.append((offset + len(line) - len(line.lstrip()), line.strip()))
        offset += len(line) + 1  # +1 for the newline join

    if not source_url:
        print(f"  ! {path.name}: no 'Source:' line found — source_url will be empty")

    return Document(
        doc_id=path.stem,
        title=title or path.stem,
        source_url=source_url,
        source_file=str(path.relative_to(PROJECT_ROOT)),
        body=body,
        sections=sections,
    )


def load_documents(input_dir: Path = INPUT_DIR) -> list[Document]:
    """Load and parse every .txt file in input_dir, sorted by filename."""
    if not input_dir.is_dir():
        raise FileNotFoundError(f"Input directory not found: {input_dir}")

    paths = sorted(p for p in input_dir.glob("*.txt") if p.stat().st_size > 0)
    if not paths:
        raise FileNotFoundError(f"No non-empty .txt files in {input_dir}")

    return [parse_document(p) for p in paths]


def sections_for_span(doc: Document, start: int, end: int) -> list[str]:
    """Section headers a chunk starts in or runs through."""
    if not doc.sections:
        return []

    spanned = [name for pos, name in doc.sections if start <= pos < end]

    # The section the chunk *starts* inside (its header may sit above `start`).
    opening = [name for pos, name in doc.sections if pos <= start]
    if opening:
        spanned.insert(0, opening[-1])

    seen: list[str] = []
    for name in spanned:
        if name not in seen:
            seen.append(name)
    return seen


def chunk_documents(
    documents: list[Document],
    chunk_size: int = CHUNK_SIZE,
    overlap: int = CHUNK_OVERLAP,
) -> list[dict]:
    """Chunk every document and attach retrieval metadata to each chunk."""
    all_chunks: list[dict] = []

    for doc in documents:
        raw_chunks = chunk_text(doc.body, chunk_size=chunk_size, overlap=overlap)
        for index, chunk in enumerate(raw_chunks):
            spanned = sections_for_span(doc, chunk["start_char"], chunk["end_char"])
            all_chunks.append(
                {
                    "chunk_id": f"{doc.doc_id}::{index}",
                    "text": chunk["text"],
                    # Flat scalar metadata — ChromaDB only accepts str/int/float/bool.
                    "metadata": {
                        "doc_id": doc.doc_id,
                        "title": doc.title,
                        "source_url": doc.source_url,
                        "source_file": doc.source_file,
                        "section": spanned[0] if spanned else "",
                        "sections": " | ".join(spanned),
                        "chunk_index": index,
                        "chunk_count": len(raw_chunks),
                        "token_count": chunk["token_count"],
                        "start_char": chunk["start_char"],
                        "end_char": chunk["end_char"],
                    },
                }
            )

    return all_chunks


def write_chunks(chunks: list[dict], output: Path, chunk_size: int, overlap: int) -> None:
    payload = {
        "config": {
            "chunk_size_tokens": chunk_size,
            "overlap_tokens": overlap,
            "tokenizer": EMBEDDING_MODEL if get_tokenizer() else "whitespace-fallback",
            "embedding_model": EMBEDDING_MODEL,
        },
        "chunk_count": len(chunks),
        "chunks": chunks,
    }
    output.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def report(
    documents: list[Document], chunks: list[dict], preview: int, seed: int
) -> None:
    print("\nDocuments")
    print("-" * 72)
    for doc in documents:
        doc_chunks = [c for c in chunks if c["metadata"]["doc_id"] == doc.doc_id]
        print(
            f"  {doc.doc_id:<28} {doc.token_count:>5} tokens  "
            f"{len(doc_chunks):>2} chunks  {len(doc.sections):>2} sections"
        )
        if not doc.source_url:
            print("      (missing source URL)")

    counts = [c["metadata"]["token_count"] for c in chunks]
    print("\nChunks")
    print("-" * 72)
    print(f"  total chunks : {len(chunks)}")
    print(f"  tokens/chunk : min {min(counts)}  max {max(counts)}  "
          f"mean {sum(counts) / len(counts):.1f}")

    if preview:
        sample = random.Random(seed).sample(chunks, min(preview, len(chunks)))
        print(f"\n{len(sample)} random chunks (seed {seed})")
        print("-" * 72)
        for chunk in sample:
            meta = chunk["metadata"]
            print(f"\n[{chunk['chunk_id']}]  {meta['token_count']} tokens")
            print(f"  doc     : {meta['title']}")
            print(f"  section : {meta['sections'] or '(none)'}")
            print(f"  source  : {meta['source_url']}")
            print(f"  text    : {chunk['text']}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-dir", type=Path, default=INPUT_DIR)
    parser.add_argument("--output", type=Path, default=OUTPUT_FILE)
    parser.add_argument("--chunk-size", type=int, default=CHUNK_SIZE)
    parser.add_argument("--overlap", type=int, default=CHUNK_OVERLAP)
    parser.add_argument(
        "--preview",
        type=int,
        default=5,
        help="how many random sample chunks to print (0 to skip)",
    )
    parser.add_argument(
        "--seed", type=int, default=42, help="seed for the random chunk sample"
    )
    args = parser.parse_args()

    if get_tokenizer() is None:
        print(
            "! Could not load the all-MiniLM-L6-v2 tokenizer; counting whitespace\n"
            "  words instead. Chunk sizes will not match what the embedder sees."
        )

    if args.chunk_size > MODEL_MAX_TOKENS:
        print(
            f"! chunk_size={args.chunk_size} exceeds all-MiniLM-L6-v2's "
            f"{MODEL_MAX_TOKENS}-token input limit.\n"
            f"  The model will embed only the first {MODEL_MAX_TOKENS} tokens of each "
            "chunk; the rest is retrievable text but not represented in the vector."
        )

    documents = load_documents(args.input_dir)
    chunks = chunk_documents(documents, args.chunk_size, args.overlap)
    write_chunks(chunks, args.output, args.chunk_size, args.overlap)

    report(documents, chunks, args.preview, args.seed)
    print(f"\nWrote {len(chunks)} chunks -> {args.output}")


if __name__ == "__main__":
    main()
