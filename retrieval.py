"""Milestone 4 -- embedding and retrieval (stages 3 and 4 of the pipeline).

    1. Document Ingestion   ingest.py         processed_data/*.txt
    2. Chunking             chunking.py       -> chunks.json
    3. Embedding + Store    THIS FILE         sentence-transformers
                                              all-MiniLM-L6-v2 -> ChromaDB
    4. Retrieval            THIS FILE         Chroma similarity search, top-k = 5
    5. Generation           (milestone 5)     gpt-oss-120b + retrieved context

Stage 3 reads the chunks produced by ingest.py, embeds each one with
all-MiniLM-L6-v2, and stores the vector alongside the chunk's text and source
metadata (title, URL, section) in a persistent ChromaDB collection. Stage 4
embeds a user query with the same model and returns the top-k nearest chunks
with their source attribution attached, ready to hand to the generator.

Run it:
    python retrieval.py --build                 # embed chunks.json into ChromaDB
    python retrieval.py --query "4c hair tips"  # retrieve top-3 for one question
    python retrieval.py --eval                  # run the 5 planning.md questions
"""

import argparse
import json
import textwrap
from dataclasses import asdict, dataclass
from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer

PROJECT_ROOT = Path(__file__).resolve().parent
CHUNKS_FILE = PROJECT_ROOT / "chunks.json"
PERSIST_DIR = PROJECT_ROOT / "chroma_db"

# From planning.md -> Retrieval Approach
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
# Raised from 3 to 5 during implementation: at k=3 the on-topic chunk for the
# 4C and length-retention questions ranked 4th, one slot outside the cutoff.
TOP_K = 5

COLLECTION_NAME = "unofficial_guide"

# The 5 test questions from planning.md -> Evaluation Plan.
EVAL_QUESTIONS = [
    "What styling techniques, maintenance practices, and product recommendations "
    "are discussed for 4C natural hair?",

    "What practices can help me retain length while maintaining healthy natural hair?",

    "I work out several times a week and don't want to wash my natural hair after "
    "every workout. How can I maintain my hairstyle between workouts?",

    "My natural hair has heat damage. What approaches should be used to adjust my "
    "routine and care for my hair afterward?",
    
    "How do hair-care recommendations differ between low-porosity and high-porosity "
    "hair, especially when it comes to products and styling?",
]


@dataclass
class RetrievedChunk:
    """One retrieved chunk plus the attribution the generator needs to cite it."""

    rank: int
    chunk_id: str
    text: str
    similarity: float
    doc_id: str
    title: str
    section: str
    source_url: str

    def to_dict(self) -> dict:
        return asdict(self)


_EMBEDDER = None


def get_embedder() -> SentenceTransformer:
    """Load all-MiniLM-L6-v2 once and reuse it."""
    global _EMBEDDER
    if _EMBEDDER is None:
        _EMBEDDER = SentenceTransformer(EMBEDDING_MODEL)
    return _EMBEDDER


def embed(texts: list[str]) -> list[list[float]]:
    """Embed texts, L2-normalized so cosine distance behaves predictably."""
    vectors = get_embedder().encode(
        texts,
        normalize_embeddings=True,
        show_progress_bar=len(texts) > 32,
    )
    return [v.tolist() for v in vectors]


def load_chunks(chunks_file: Path = CHUNKS_FILE) -> list[dict]:
    """Read the chunks written by ingest.py."""
    if not chunks_file.exists():
        raise FileNotFoundError(
            f"{chunks_file} not found — run `python ingest.py` first."
        )
    payload = json.loads(chunks_file.read_text(encoding="utf-8"))
    chunks = payload.get("chunks", [])
    if not chunks:
        raise ValueError(f"{chunks_file} contains no chunks.")
    return chunks


def get_client(persist_dir: Path = PERSIST_DIR) -> chromadb.ClientAPI:
    """A ChromaDB client that persists to disk, so we embed only once."""
    return chromadb.PersistentClient(path=str(persist_dir))


def build_index(
    chunks_file: Path = CHUNKS_FILE,
    persist_dir: Path = PERSIST_DIR,
    collection_name: str = COLLECTION_NAME,
    rebuild: bool = False,
) -> chromadb.Collection:
    """Stage 3: embed every chunk and store it in ChromaDB with its metadata."""
    chunks = load_chunks(chunks_file)
    client = get_client(persist_dir)

    existing = {c.name for c in client.list_collections()}
    if collection_name in existing:
        collection = client.get_collection(collection_name, embedding_function=None)
        if not rebuild and collection.count() == len(chunks):
            print(
                f"Collection '{collection_name}' already holds {collection.count()} "
                "chunks — reusing it (pass --rebuild to re-embed)."
            )
            return collection
        # Chunk count changed (or --rebuild): drop it so we never mix stale
        # vectors from an older chunking run with new ones.
        print(f"Rebuilding collection '{collection_name}'...")
        client.delete_collection(collection_name)

    collection = client.create_collection(
        collection_name,
        # Cosine matches how all-MiniLM-L6-v2 embeddings are meant to be compared.
        configuration={"hnsw": {"space": "cosine"}},
        # We pass our own vectors, so Chroma must not embed anything itself.
        embedding_function=None,
    )

    texts = [c["text"] for c in chunks]
    print(f"Embedding {len(texts)} chunks with {EMBEDDING_MODEL}...")
    embeddings = embed(texts)

    collection.add(
        ids=[c["chunk_id"] for c in chunks],
        documents=texts,
        embeddings=embeddings,
        metadatas=[c["metadata"] for c in chunks],
    )
    print(f"Stored {collection.count()} chunks in {persist_dir}")
    return collection


def get_collection(
    persist_dir: Path = PERSIST_DIR, collection_name: str = COLLECTION_NAME
) -> chromadb.Collection:
    """Open the existing collection for querying."""
    client = get_client(persist_dir)
    if collection_name not in {c.name for c in client.list_collections()}:
        raise RuntimeError(
            f"Collection '{collection_name}' does not exist — "
            "run `python retrieval.py --build` first."
        )
    return client.get_collection(collection_name, embedding_function=None)


def retrieve(
    query: str,
    top_k: int = TOP_K,
    collection: chromadb.Collection | None = None,
    min_similarity: float = 0.0,
) -> list[RetrievedChunk]:
    """Stage 4: return the top_k chunks most similar to the query.

    min_similarity drops weak matches (cosine similarity below the threshold);
    it defaults to 0.0, which keeps everything. Milestone 5 can raise it so the
    generator refuses out-of-scope questions instead of answering from noise.
    """
    if not query.strip():
        return []
    if collection is None:
        collection = get_collection()

    response = collection.query(
        query_embeddings=embed([query]),
        n_results=min(top_k, collection.count()),
        include=["documents", "metadatas", "distances"],
    )

    results: list[RetrievedChunk] = []
    ids = response["ids"][0]
    documents = response["documents"][0]
    metadatas = response["metadatas"][0]
    distances = response["distances"][0]

    for rank, (chunk_id, text, meta, distance) in enumerate(
        zip(ids, documents, metadatas, distances), start=1
    ):
        # Chroma returns cosine *distance*; similarity is 1 - distance.
        similarity = 1.0 - float(distance)
        if similarity < min_similarity:
            continue
        results.append(
            RetrievedChunk(
                rank=rank,
                chunk_id=chunk_id,
                text=text,
                similarity=round(similarity, 4),
                doc_id=str(meta.get("doc_id", "")),
                title=str(meta.get("title", "")),
                section=str(meta.get("sections") or meta.get("section") or ""),
                source_url=str(meta.get("source_url", "")),
            )
        )
    return results


def format_results(results: list[RetrievedChunk], width: int = 88) -> str:
    """Human-readable retrieval output for the terminal and the README."""
    if not results:
        return "  (no chunks retrieved)"

    lines = []
    for r in results:
        lines.append(f"\n  [{r.rank}] {r.chunk_id}   similarity {r.similarity:.3f}")
        lines.append(f"      doc     : {r.title}")
        lines.append(f"      section : {r.section or '(none)'}")
        lines.append(f"      source  : {r.source_url}")
        body = " ".join(r.text.split())
        for line in textwrap.wrap(body, width=width - 16):
            lines.append(f"      {line}")
    return "\n".join(lines)


def run_eval(top_k: int = TOP_K) -> None:
    """Run the 5 planning.md questions and print what retrieval returns."""
    collection = get_collection()
    for i, question in enumerate(EVAL_QUESTIONS, start=1):
        print("\n" + "=" * 88)
        print(f"Q{i}: {question}")
        print("=" * 88)
        results = retrieve(question, top_k=top_k, collection=collection)
        print(format_results(results))
        sources = sorted({r.doc_id for r in results})
        print(f"\n  documents hit: {', '.join(sources)}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--build", action="store_true", help="embed chunks into ChromaDB")
    parser.add_argument("--rebuild", action="store_true", help="force re-embedding")
    parser.add_argument("--query", type=str, help="retrieve chunks for one question")
    parser.add_argument("--eval", action="store_true", help="run the 5 test questions")
    parser.add_argument("--top-k", type=int, default=TOP_K)
    parser.add_argument("--chunks-file", type=Path, default=CHUNKS_FILE)
    parser.add_argument("--persist-dir", type=Path, default=PERSIST_DIR)
    args = parser.parse_args()

    if args.build or args.rebuild:
        build_index(args.chunks_file, args.persist_dir, rebuild=args.rebuild)

    if args.query:
        results = retrieve(args.query, top_k=args.top_k)
        print(f"\nQuery: {args.query}")
        print(format_results(results))

    if args.eval:
        run_eval(top_k=args.top_k)

    if not (args.build or args.rebuild or args.query or args.eval):
        parser.print_help()


if __name__ == "__main__":
    main()
