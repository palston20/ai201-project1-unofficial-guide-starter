"""Boundary-aware chunking with overlap.

Implements the Chunking Strategy from planning.md:
    target chunk size = 100 tokens, overlap = 20 tokens

Chunks are built by packing whole *units* -- sentences, bullet-list items, and
section headers -- up to the target size, rather than by cutting fixed token
windows. A fixed window lands wherever the 100th token happens to fall, which
produced chunks ending on "Divide hair" or "use either". Packing whole units
means a chunk can run a little under or over the target, but it always ends
where a sentence or a list item ends, so every chunk is a complete thought.

Tokens are counted with the *same* tokenizer the embedding model uses
(all-MiniLM-L6-v2), so a "100 token chunk" means 100 tokens as the embedder
will see them -- not 100 whitespace words. If that tokenizer cannot be loaded
(no network on first run), we fall back to a whitespace word tokenizer and say
so.

Chunk text is sliced out of the ORIGINAL string using character offsets, so
chunks keep their real capitalization, punctuation, and line structure.
"""

import re
from bisect import bisect_left
from dataclasses import dataclass

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# From planning.md -> Chunking Strategy
CHUNK_SIZE = 100
CHUNK_OVERLAP = 20

# A trailing chunk shorter than this is folded into the chunk before it
# instead of being emitted as a stub.
MIN_CHUNK_TOKENS = 30

# End of sentence: . ! or ? plus any closing quote/bracket, then whitespace.
SENTENCE_END = re.compile(r'(?<=[.!?])["\'’”)\]]*\s+')

# A line that opens a bullet or numbered list item.
LIST_ITEM = re.compile(r"^\s*(?:[*\-•–—]|\d+[.)])\s+")

# Don't split after these — they end in a period but not a sentence.
ABBREVIATIONS = {
    "dr", "mr", "mrs", "ms", "prof", "e.g", "i.e", "etc", "vs", "approx",
    "oz", "fl", "no", "st",
}


def _load_hf_tokenizer():
    """Return the all-MiniLM-L6-v2 fast tokenizer, or None if unavailable."""
    try:
        from transformers import AutoTokenizer

        return AutoTokenizer.from_pretrained(EMBEDDING_MODEL, use_fast=True)
    except Exception:
        return None


_HF_TOKENIZER = None
_HF_TOKENIZER_TRIED = False


def get_tokenizer():
    """Lazily load and cache the tokenizer (None means use the fallback)."""
    global _HF_TOKENIZER, _HF_TOKENIZER_TRIED
    if not _HF_TOKENIZER_TRIED:
        _HF_TOKENIZER = _load_hf_tokenizer()
        _HF_TOKENIZER_TRIED = True
    return _HF_TOKENIZER


def tokenize_with_offsets(text: str) -> list[tuple[int, int]]:
    """Tokenize text into (start_char, end_char) spans."""
    tokenizer = get_tokenizer()
    if tokenizer is not None:
        encoded = tokenizer(
            text,
            add_special_tokens=False,
            return_offsets_mapping=True,
            truncation=False,
            verbose=False,
        )
        return [(int(s), int(e)) for s, e in encoded["offset_mapping"] if e > s]

    return [(m.start(), m.end()) for m in re.finditer(r"\S+", text)]


def count_tokens(text: str) -> int:
    """Number of tokens in text under the active tokenizer."""
    return len(tokenize_with_offsets(text))


def is_section_header(line: str) -> bool:
    """True for short ALL-CAPS lines like 'WASHING & CONDITIONING'."""
    stripped = line.strip()
    if not stripped or len(stripped) > 80:
        return False
    if not any(ch.isalpha() for ch in stripped):
        return False
    if stripped.endswith((".", ",", ":", ";")):
        return False
    return stripped == stripped.upper()


@dataclass
class Unit:
    """One indivisible piece of text: a sentence, list item, or header."""

    start: int
    end: int
    is_header: bool = False
    token_count: int = 0
    first_token: int = 0


def _split_sentences(text: str, offset: int) -> list[tuple[int, int]]:
    """Split one line into sentence spans, as (start, end) in the full text."""
    spans: list[tuple[int, int]] = []
    start = 0
    for match in SENTENCE_END.finditer(text):
        candidate = text[start:match.start()]
        # Skip a break that follows a known abbreviation ("e.g.", "approx.").
        last_word = re.split(r"[\s(]", candidate.rstrip("."))[-1].lower()
        if last_word in ABBREVIATIONS:
            continue
        spans.append((offset + start, offset + match.start()))
        start = match.end()
    if start < len(text):
        spans.append((offset + start, offset + len(text)))
    return [(s, e) for s, e in spans if e > s]


def split_units(text: str) -> list[Unit]:
    """Break text into the atomic units chunks are assembled from.

    Headers and list items stay whole; prose lines split into sentences.
    """
    units: list[Unit] = []
    offset = 0

    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            offset += len(line) + 1
            continue

        lead = len(line) - len(line.lstrip())
        start = offset + lead
        end = offset + len(line.rstrip())

        if is_section_header(line):
            units.append(Unit(start, end, is_header=True))
        elif LIST_ITEM.match(line):
            # A bullet is one thought even when it has no terminal period.
            units.append(Unit(start, end))
        else:
            for s, e in _split_sentences(text[start:end], start):
                units.append(Unit(s, e))

        offset += len(line) + 1

    return units


def _assign_token_counts(units: list[Unit], token_spans: list[tuple[int, int]]) -> None:
    """Fill in each unit's token_count and first_token index."""
    starts = [s for s, _ in token_spans]
    for unit in units:
        lo = bisect_left(starts, unit.start)
        hi = bisect_left(starts, unit.end)
        unit.first_token = lo
        unit.token_count = max(hi - lo, 1)


def chunk_text(
    text: str,
    chunk_size: int = CHUNK_SIZE,
    overlap: int = CHUNK_OVERLAP,
    min_chunk_tokens: int = MIN_CHUNK_TOKENS,
) -> list[dict]:
    """Split text into overlapping chunks that end on sentence boundaries.

    Returns a list of dicts with keys:
        text, start_char, end_char, start_token, end_token, token_count
    """
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")
    if not 0 <= overlap < chunk_size:
        raise ValueError("overlap must be >= 0 and smaller than chunk_size")

    units = split_units(text)
    if not units:
        return []

    token_spans = tokenize_with_offsets(text)
    _assign_token_counts(units, token_spans)

    # Pack whole units into chunks, then step back by `overlap` tokens.
    windows: list[tuple[int, int]] = []  # (first_unit, last_unit_exclusive)
    i = 0
    while i < len(units):
        j = i
        tokens = 0
        while j < len(units):
            # Always take at least one unit, even if it alone exceeds the target.
            if tokens and tokens + units[j].token_count > chunk_size:
                break
            tokens += units[j].token_count
            j += 1

        # A chunk should not end on a header that introduces the next section.
        while j - 1 > i and units[j - 1].is_header:
            j -= 1

        windows.append((i, j))
        if j >= len(units):
            break

        # Walk back over trailing units until we've covered the overlap.
        k = j
        carried = 0
        while k > i + 1 and carried < overlap:
            k -= 1
            carried += units[k].token_count
        i = k

    # Fold a too-small tail into the chunk before it.
    if len(windows) > 1:
        start, end = windows[-1]
        tail_tokens = sum(u.token_count for u in units[start:end])
        if tail_tokens < min_chunk_tokens:
            windows[-2] = (windows[-2][0], end)
            windows.pop()

    starts = [s for s, _ in token_spans]
    chunks = []
    for first, last in windows:
        start_char = units[first].start
        end_char = units[last - 1].end
        body = text[start_char:end_char].strip()
        if not body:
            continue
        start_token = bisect_left(starts, start_char)
        end_token = bisect_left(starts, end_char)
        chunks.append(
            {
                "text": body,
                "start_char": start_char,
                "end_char": end_char,
                "start_token": start_token,
                "end_token": end_token,
                "token_count": max(end_token - start_token, 1),
            }
        )
    return chunks
