"""Utility functions for tutorials/tutorial_pydanticAI/pydanticai.example notebook."""

import hashlib
import math
import re
from pathlib import Path
from typing import Any

from pydantic_ai import ModelRetry


# #########################################################################
# Code for chunking and embeddings.
# #########################################################################
_DIM = 256


def _stable_index(token: str, dim: int = _DIM) -> int:
    h = hashlib.md5(token.encode("utf-8")).digest()
    return int.from_bytes(h[:4], "little") % dim


def embed(text: str) -> list[float]:
    vec = [0.0] * _DIM
    tokens = re.findall(r"[a-z0-9]+", text.lower())
    for t in tokens:
        vec[_stable_index(t)] += 1.0
    norm = math.sqrt(sum(x * x for x in vec)) or 1.0
    return [x / norm for x in vec]


def dot(a: list[float], b: list[float]) -> float:
    return sum(x * y for x, y in zip(a, b))


def chunk_docs(docs: list[dict], doc_chunk_cls: Any, *, max_chars: int = 600) -> list[Any]:
    chunks: list[Any] = []
    for d in docs:
        text = d["text"].strip()
        parts = [text[i : i + max_chars] for i in range(0, len(text), max_chars)]
        for j, part in enumerate(parts):
            chunks.append(
                doc_chunk_cls(
                    doc_id=d["doc_id"],
                    chunk_id=j,
                    text=part,
                    vector=embed(part),
                )
            )
    return chunks


def search_chunks(
    chunks: list[Any], query: str, doc_match_cls: Any, *, top_k: int = 3
) -> list[Any]:
    q_vec = embed(query)
    scored: list[Any] = []
    for ch in chunks:
        score = dot(q_vec, ch.vector)
        scored.append(
            doc_match_cls(
                doc_id=ch.doc_id,
                chunk_id=ch.chunk_id,
                score=score,
                text=ch.text,
            )
        )
    scored.sort(key=lambda m: (-m.score, m.doc_id, m.chunk_id))
    return scored[:top_k]


# #########################################################################
# Code for tools and validators.
# #########################################################################
def search_docs(
    ctx: Any,
    query: str,
    top_k: int = 3,
    *,
    doc_match_cls: Any,
) -> list[Any]:
    return search_chunks(ctx.deps.chunks, query, doc_match_cls, top_k=top_k)


def enforce_sources(result: Any) -> Any:
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
        raise ModelRetry("You referenced docs/policies but did not include sources.")
    if len(result.sources) > 3:
        raise ModelRetry("Too many sources. Max 3.")
    seen = set()
    for s in result.sources:
        key = (s.doc_id, s.chunk_id, s.quote)
        if key in seen:
            raise ModelRetry("Duplicate sources. Keep sources unique.")
        seen.add(key)
    return result


# #########################################################################
# Code for async notebook wrappers.
# #########################################################################
async def ask(query: str, deps: Any, agent: Any) -> Any:
    res = await agent.run(query, deps=deps)
    return res.output


async def stream_demo(stream_agent: Any) -> None:
    if not hasattr(stream_agent, "run_stream"):
        res = await stream_agent.run("What are unit tests?")
        print(res.output)
        return
    async with stream_agent.run_stream("What are unit tests?") as s:
        async for chunk in s.stream_text():
            print(chunk, end="", flush=True)
        print("\n")


# #########################################################################
# Code for guardrails and dynamic data loading.
# #########################################################################
IN_SCOPE_TERMS = {
    "atlas",
    "billing",
    "invoice",
    "plan",
    "support",
    "ticket",
    "sync",
    "security",
    "limits",
    "storage",
    "2fa",
}


def in_scope(question: str) -> bool:
    q = question.lower()
    return any(term in q for term in IN_SCOPE_TERMS)


async def run_guarded(
    question: str,
    deps: Any,
    agent: Any,
    answer_with_sources_cls: Any,
    *,
    history: Any = None,
) -> Any:
    if not in_scope(question):
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
    """
    Load markdown docs from a directory into a standard format:
    {doc_id, title, text}.
    """
    docs = []
    for p in sorted(docs_dir.glob("*.md")):
        docs.append(
            {
                "doc_id": p.stem,
                "title": p.stem.replace("_", " ").title(),
                "text": p.read_text(encoding="utf-8"),
            }
        )
    return docs
