"""
Utilities for pydanticai.example.ipynb / pydanticai.example.py.
"""

from __future__ import annotations

import hashlib
import math
import re
from pathlib import Path
from typing import Any


def stable_index(token: str, dim: int = 256) -> int:
    h = hashlib.md5(token.encode("utf-8")).digest()
    return int.from_bytes(h[:4], "little") % dim


def embed(text: str, dim: int = 256) -> list[float]:
    vec = [0.0] * dim
    tokens = re.findall(r"[a-z0-9]+", text.lower())
    for token in tokens:
        vec[stable_index(token, dim=dim)] += 1.0
    norm = math.sqrt(sum(x * x for x in vec)) or 1.0
    return [x / norm for x in vec]


def dot(a: list[float], b: list[float]) -> float:
    return sum(x * y for x, y in zip(a, b))


def chunk_docs(
    docs: list[dict],
    doc_chunk_cls: Any,
    max_chars: int = 600,
    dim: int = 256,
) -> list[Any]:
    chunks: list[Any] = []
    for doc in docs:
        text = doc["text"].strip()
        parts = [text[i : i + max_chars] for i in range(0, len(text), max_chars)]
        for chunk_id, part in enumerate(parts):
            chunks.append(
                doc_chunk_cls(
                    doc_id=doc["doc_id"],
                    chunk_id=chunk_id,
                    text=part,
                    vector=embed(part, dim=dim),
                )
            )
    return chunks


def search_chunks(
    chunks: list[Any],
    query: str,
    doc_match_cls: Any,
    top_k: int = 3,
    dim: int = 256,
) -> list[Any]:
    query_vector = embed(query, dim=dim)
    scored: list[Any] = []
    for chunk in chunks:
        score = dot(query_vector, chunk.vector)
        scored.append(
            doc_match_cls(
                doc_id=chunk.doc_id,
                chunk_id=chunk.chunk_id,
                score=score,
                text=chunk.text,
            )
        )
    scored.sort(key=lambda match: (-match.score, match.doc_id, match.chunk_id))
    return scored[:top_k]


def search_docs(
    ctx: Any,
    query: str,
    top_k: int = 3,
    *,
    search_chunks_fn: Any,
) -> list[Any]:
    return search_chunks_fn(ctx.deps.chunks, query, top_k=top_k)


def enforce_sources(result: Any, *, model_retry_cls: Any) -> Any:
    answer_l = result.answer.lower()
    mentions_docs = any(
        tok in answer_l
        for tok in [
            "according",
            "docs",
            "document",
            "settings",
            "billing",
            "invoice",
            "plan",
            "limit",
        ]
    )
    if mentions_docs and not result.sources:
        raise model_retry_cls("You referenced docs/policies but did not include sources.")

    if len(result.sources) > 3:
        raise model_retry_cls("Too many sources. Max 3.")

    seen = set()
    for source in result.sources:
        key = (source.doc_id, source.chunk_id, source.quote)
        if key in seen:
            raise model_retry_cls("Duplicate sources. Keep sources unique.")
        seen.add(key)

    return result


async def ask(agent: Any, query: str, deps: Any) -> Any:
    res = await agent.run(query, deps=deps)
    return res.output


async def stream_demo(stream_agent: Any) -> None:
    if not hasattr(stream_agent, "run_stream"):
        res = await stream_agent.run("What are unit tests?")
        print(res.output)
        return

    async with stream_agent.run_stream("What are unit tests?") as stream:
        async for chunk in stream.stream_text():
            print(chunk, end="", flush=True)
        print("\n")


def in_scope(question: str, *, in_scope_terms: set[str]) -> bool:
    q = question.lower()
    return any(term in q for term in in_scope_terms)


async def run_guarded(
    agent: Any,
    question: str,
    deps: Any,
    answer_with_sources_cls: Any,
    in_scope_fn: Any,
    history: Any = None,
) -> Any:
    if not in_scope_fn(question):
        return answer_with_sources_cls(
            answer="I can only help with Atlas product documentation and support questions.",
            sources=[],
            follow_up_questions=[
                "Do you have a question about Atlas setup, billing, or support?"
            ],
        )
    result = await agent.run(question, deps=deps, message_history=history)
    return result.output


def load_docs(docs_dir: Path) -> list[dict]:
    docs = []
    for path in sorted(docs_dir.glob("*.md")):
        docs.append(
            {
                "doc_id": path.stem,
                "title": path.stem.replace("_", " ").title(),
                "text": path.read_text(encoding="utf-8"),
            }
        )
    return docs
