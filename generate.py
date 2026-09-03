"""Milestone 5 -- grounded generation (stage 5 of the pipeline).

    1. Document Ingestion   ingest.py      processed_data/*.txt
    2. Chunking             chunking.py    -> chunks.json
    3. Embedding + Store    retrieval.py   all-MiniLM-L6-v2 -> ChromaDB
    4. Retrieval            retrieval.py   Chroma similarity search, top-k = 5
    5. Generation           THIS FILE      gpt-oss-120b + retrieved context
       Interface            app.py         Streamlit

Grounding is enforced in three places, not just by asking the model nicely:

  1. A relevance gate BEFORE the model is called. Chunks scoring below
     MIN_SIMILARITY are dropped, and if nothing survives we return a refusal
     without spending a request. Out-of-scope questions score 0.02-0.30 here
     while real questions score 0.62-0.80, so the gate separates them cleanly.
  2. The context block is numbered, and the system prompt requires every claim
     to carry the [n] of the passage it came from.
  3. The source list shown to the user is built from the retrieved chunks in
     code -- the model cannot invent a citation, because it never writes the
     source list itself.

gpt-oss-120b is a reasoning model: it returns `content` plus a separate
`reasoning` field, and if max_tokens is too small the whole budget goes to
reasoning and `content` comes back empty. MAX_TOKENS is sized for both.

Run it:
    python generate.py --question "How do I fight humidity?"
    python generate.py --eval        # the 5 planning.md test questions
"""

import argparse
import os
import re
import textwrap
from dataclasses import dataclass, field
from pathlib import Path

import httpx
from dotenv import load_dotenv

from retrieval import (
    EVAL_QUESTIONS,
    TOP_K,
    RetrievedChunk,
    get_collection,
    retrieve,
)

PROJECT_ROOT = Path(__file__).resolve().parent

# planning.md -> Architecture, stage 5. Served through the Hugging Face
# Inference Providers router, which speaks the OpenAI chat-completions format.
MODEL = "openai/gpt-oss-120b"
API_URL = "https://router.huggingface.co/v1/chat/completions"

# Any of these env var names will do, so the .env does not have to be renamed.
TOKEN_VARS = ("HF_TOKEN", "HUGGINGFACE_API_KEY", "OPENAI_API_KEY")

# Cosine similarity below this is treated as "not in the guide". Measured:
# the 5 eval questions score 0.62-0.80, off-topic questions score 0.02-0.30.
MIN_SIMILARITY = 0.45

# gpt-oss-120b spends part of this budget on reasoning before writing content.
MAX_TOKENS = 1200
TEMPERATURE = 0.2
REASONING_EFFORT = "low"

REFUSAL = (
    "I don't have anything in the guide that answers that. This guide only "
    "covers natural and curly hair care — styling, washing, porosity, "
    "protective styles, heat damage, humidity, and length retention — drawn "
    "from a fixed set of blogs and Reddit threads."
)

SYSTEM_PROMPT = """\
You are the Unofficial Guide to natural and curly hair care. You answer \
strictly from a set of numbered passages retrieved from community sources \
(Reddit threads, forums, and hair-care blogs).

GROUNDING RULES — these override any other instinct you have:
1. Use ONLY the numbered passages provided. Do not add hair-care knowledge \
from your training, even if you are confident it is correct and even if the \
passages seem incomplete.
2. Every factual claim must cite the passage it came from, written as [1], \
[2], etc. A sentence with no citation is not allowed.
3. If the passages do not answer the question, say so plainly and state what \
they do cover instead. Do not guess, and do not pad the answer with general \
advice to appear helpful.
4. If the passages disagree with each other, present both positions and \
attribute each one, rather than silently picking a winner.
5. Most of these sources are individual people describing what worked for \
them. Report them that way — "one commenter recommends...", "the blog \
suggests..." — and never present a personal routine as an established fact or \
a guaranteed result. Where a passage itself flags something as a personal \
experience, keep that framing.
6. Never recommend a specific product unless a passage names it.

STYLE:
- Answer directly, then support it. No preamble like "Based on the passages".
- Prefer short paragraphs or bullets. Keep it under about 200 words.
- Do not write a "Sources" section — the interface adds one from the \
retrieved passages.
"""

USER_TEMPLATE = """\
Passages retrieved from the guide:

{context}

Question: {question}

Answer using only the passages above, citing them as [n]."""


@dataclass
class GeneratedAnswer:
    """A grounded answer plus the sources it was allowed to draw on."""

    question: str
    answer: str
    chunks: list[RetrievedChunk] = field(default_factory=list)
    refused: bool = False
    cited_ranks: list[int] = field(default_factory=list)

    @property
    def sources(self) -> list[RetrievedChunk]:
        """The chunks the answer actually cited (all of them if it cited none)."""
        if not self.cited_ranks:
            return self.chunks
        return [c for c in self.chunks if c.rank in self.cited_ranks]

    @property
    def source_documents(self) -> list[tuple[str, str]]:
        """Unique (title, url) pairs behind the answer, in citation order."""
        seen: list[tuple[str, str]] = []
        for chunk in self.sources:
            pair = (chunk.title, chunk.source_url)
            if pair not in seen:
                seen.append(pair)
        return seen


def get_token() -> str:
    """Read the API token from the environment or .env."""
    load_dotenv(PROJECT_ROOT / ".env")
    for name in TOKEN_VARS:
        token = os.environ.get(name, "").strip()
        if token and token != "your_key_here":
            return token
    raise RuntimeError(
        "No API token found. Add one to .env as:\n"
        "    HF_TOKEN=hf_...\n"
        "Get a token at https://huggingface.co/settings/tokens "
        "(it needs the 'Make calls to Inference Providers' permission)."
    )


def build_context(chunks: list[RetrievedChunk]) -> str:
    """Format retrieved chunks as the numbered block the prompt refers to."""
    blocks = []
    for chunk in chunks:
        header = f"[{chunk.rank}] {chunk.title}"
        if chunk.section:
            header += f" — {chunk.section}"
        blocks.append(f"{header}\n{chunk.text}")
    return "\n\n".join(blocks)


def build_messages(question: str, chunks: list[RetrievedChunk]) -> list[dict]:
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {
            "role": "user",
            "content": USER_TEMPLATE.format(
                context=build_context(chunks), question=question.strip()
            ),
        },
    ]


def call_model(messages: list[dict], timeout: float = 120.0) -> str:
    """Send the prompt to gpt-oss-120b and return the answer text."""
    response = httpx.post(
        API_URL,
        headers={"Authorization": f"Bearer {get_token()}"},
        json={
            "model": MODEL,
            "messages": messages,
            "max_tokens": MAX_TOKENS,
            "temperature": TEMPERATURE,
            "reasoning_effort": REASONING_EFFORT,
        },
        timeout=timeout,
    )
    if response.status_code != 200:
        raise RuntimeError(
            f"{MODEL} request failed ({response.status_code}): {response.text[:300]}"
        )

    message = response.json()["choices"][0]["message"]
    content = (message.get("content") or "").strip()
    if not content:
        # All of max_tokens went to the reasoning channel.
        raise RuntimeError(
            "The model returned reasoning but no answer — raise MAX_TOKENS "
            f"(currently {MAX_TOKENS}) or lower REASONING_EFFORT."
        )
    return content


def find_citations(answer: str, chunk_count: int) -> list[int]:
    """Pull the [n] markers out of an answer, keeping only valid ones."""
    found = {int(n) for n in re.findall(r"\[(\d+)\]", answer)}
    return sorted(n for n in found if 1 <= n <= chunk_count)


def answer_question(
    question: str,
    top_k: int = TOP_K,
    min_similarity: float = MIN_SIMILARITY,
    collection=None,
) -> GeneratedAnswer:
    """Retrieve, gate on relevance, then generate a grounded answer."""
    question = question.strip()
    if not question:
        return GeneratedAnswer(question, "Ask a question to get started.", refused=True)

    chunks = retrieve(
        question,
        top_k=top_k,
        collection=collection,
        min_similarity=min_similarity,
    )

    # Structural grounding: nothing relevant means we refuse without calling
    # the model at all, so it never gets the chance to answer from memory.
    if not chunks:
        return GeneratedAnswer(question, REFUSAL, refused=True)

    answer = call_model(build_messages(question, chunks))
    return GeneratedAnswer(
        question=question,
        answer=answer,
        chunks=chunks,
        cited_ranks=find_citations(answer, len(chunks)),
    )


def format_answer(result: GeneratedAnswer, width: int = 88) -> str:
    """Answer + source list, for the terminal."""
    lines = []
    for paragraph in result.answer.split("\n"):
        lines.extend(textwrap.wrap(paragraph, width=width) or [""])

    if result.refused:
        return "\n".join(lines)

    lines.append("")
    lines.append("Sources")
    for i, (title, url) in enumerate(result.source_documents, start=1):
        lines.append(f"  {i}. {title}")
        lines.append(f"     {url}")

    used = ", ".join(f"[{c.rank}] {c.chunk_id}" for c in result.sources)
    lines.append(f"\n  passages cited: {used or '(none)'}")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--question", type=str, help="one question to answer")
    parser.add_argument("--eval", action="store_true", help="run the 5 test questions")
    parser.add_argument("--top-k", type=int, default=TOP_K)
    parser.add_argument("--min-similarity", type=float, default=MIN_SIMILARITY)
    args = parser.parse_args()

    questions = []
    if args.question:
        questions.append(args.question)
    if args.eval:
        questions.extend(EVAL_QUESTIONS)
    if not questions:
        parser.print_help()
        return

    collection = get_collection()
    for question in questions:
        print("\n" + "=" * 88)
        print(f"Q: {question}")
        print("=" * 88)
        result = answer_question(
            question,
            top_k=args.top_k,
            min_similarity=args.min_similarity,
            collection=collection,
        )
        print(format_answer(result))


if __name__ == "__main__":
    main()
