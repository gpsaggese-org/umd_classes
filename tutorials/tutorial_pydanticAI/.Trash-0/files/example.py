# %% [markdown]
# # PydanticAI Example Notebook (End-to-End)
# 
# This notebook shows an end-to-end “mini support assistant” built with PydanticAI.
# 
# We will:
# 1. Create a tiny support-document dataset (self-contained)
# 2. Build a lightweight retrieval function (RAG-style)
# 3. Use PydanticAI tools + dependencies to ground responses
# 4. Enforce citation rules with an output validator
# 5. Run async queries safely inside a notebook

# %% [markdown]
# ## Table of Contents
# 
# 1. Setup & Configuration
# 2. Data generation and Scenario
# 3. Build PydanticAI agent
# 4. Streaming data
# 5. Conversation memory
# 6. Guardrails
# 7. Dynamic Updates
# 8. Personalization

# %% [markdown]
# ## Setup
# 
# Install the few dependencies needed for a clean, runnable demo.
# 

# %%
# Run this cell
try:
    get_ipython().run_line_magic("pip", "install -q pydantic-ai pydantic python-dotenv nest_asyncio")
except Exception as e:
    print("pip install failed (continuing):", e)


# %% [markdown]
# ## Configuration (.env)
# 
# Load environment variables and print the chosen model and key status.
# 

# %%
import os
from dataclasses import dataclass
from dotenv import load_dotenv, find_dotenv
import nest_asyncio

nest_asyncio.apply()  # helps in some notebook environments

load_dotenv(find_dotenv(usecwd=True), override=True)

MODEL_ID = os.getenv("PYDANTIC_AI_MODEL", "openai:gpt-4o-mini")
print("MODEL_ID:", MODEL_ID)
print("OPENAI_API_KEY set:", bool(os.getenv("OPENAI_API_KEY")))

# %% [markdown]
# ## Data and Scenario
# 
# We build a tiny product docs corpus to keep the tutorial self-contained.
# 
# We will build a tiny documentation set for an imaginary product called **Atlas**.
# 

# %% [markdown]
# **This cell will:**
# - create the docs directory
# - write markdown files if they do not exist
# 

# %% [markdown]
# ### What this cell does
# 
# - Creates a local folder `example_dataset/` and writes a small set of **synthetic product/support documents** as Markdown files.
# - Each file represents a support knowledge-base article (billing, troubleshooting, security, limits, etc.).
# - The dataset is intentionally small but diverse so retrieval can return the *right* document depending on the question.
# 
# ### Why this matters for PydanticAI
# 
# PydanticAI becomes most useful when the agent is grounded in external context (RAG-style).  
# These documents act as that context. In the next steps, we will:
# 
# 1. Load these Markdown files into memory
# 2. Retrieve relevant chunks for a user query
# 3. Use a PydanticAI agent + tools to answer using retrieved text
# 4. Return a structured output with citations

# %%
# Run this cell
DOCS_DIR = Path("example_dataset/")
DOCS_DIR.mkdir(parents=True, exist_ok=True)

DOCS = {
    "overview.md": '''
# Atlas Overview

Atlas is a data sync service for small teams. It connects to CSV files and cloud buckets and keeps datasets up to date.

Getting started
- Create a workspace.
- Add a data source.
- Run the first sync.

Limits
- File uploads up to 50 MB.
- Up to 5 data sources on the Starter plan.
''',
    "billing.md": '''
# Billing and Plans

Plans
- Starter: $20 per month, 5 data sources, email support.
- Team: $80 per month, 25 data sources, priority email support.
- Enterprise: custom pricing, SSO, dedicated success manager.

Invoices
- Invoices are issued on the first of each month.
- You can download invoices from Settings > Billing.
''',
    "troubleshooting.md": '''
# Troubleshooting

Common issues
- Sync stuck at 0%: check your source credentials and try again.
- CSV upload fails: ensure the file is under 50 MB and encoded in UTF-8.
- Duplicate rows: enable the "deduplicate" toggle on the source.
''',
    "security.md": '''
# Security

Authentication
- Atlas supports two-factor authentication (2FA) for Team and Enterprise plans.
- Enable it under Settings > Security.

Data retention
- Deleted sources are retained for 30 days.
''',
    "limits.md": '''
# Usage Limits

Rate limits
- API requests are limited to 120 per minute on Team.
- Starter is limited to 30 per minute.

Storage
- Starter: 10 GB total storage.
- Team: 200 GB total storage.
''',
    "support.md": '''
# Support

Support channels
- Starter: email support, replies within 2 business days.
- Team: priority email support, replies within 4 business hours.
- Enterprise: dedicated success manager and 24/7 support.

Escalations
- Use the support portal to open a ticket.
''',
}

for name, text in DOCS.items():
    path = DOCS_DIR / name
    if not path.exists():
        path.write_text(text.strip() + "\n")

print("Docs directory:", DOCS_DIR)
print("Files:", [p.name for p in DOCS_DIR.glob("*.md")])


# %% [markdown]
# ## Parse and preprocess docs
# 
# Chunk the docs and build simple local embeddings for retrieval.
# 

# %%
from pathlib import Path

DOCS_DIR = Path("example_dataset/")

docs = []
for p in sorted(DOCS_DIR.glob("*.md")):
    docs.append({
        "doc_id": p.stem,      # e.g., "billing"
        "title": p.stem.replace("_", " ").title(),
        "text": p.read_text(encoding="utf-8")
    })

print("Loaded docs:", len(docs))
print("Example doc:", docs[0]["doc_id"])

# %% [markdown]
# ## Build a lightweight search index
# 
# Use cosine similarity over hashed embeddings to find relevant chunks.
# 

# %%
import re, math, hashlib
from dataclasses import dataclass
from pydantic import BaseModel
from typing import List

_DIM = 256  # bigger helps a bit for tiny corpora

def _stable_index(token: str, dim: int = _DIM) -> int:
    h = hashlib.md5(token.encode("utf-8")).digest()
    return int.from_bytes(h[:4], "little") % dim

def _embed(text: str) -> list[float]:
    vec = [0.0] * _DIM
    tokens = re.findall(r"[a-z0-9]+", text.lower())
    for t in tokens:
        vec[_stable_index(t)] += 1.0
    norm = math.sqrt(sum(x * x for x in vec)) or 1.0
    return [x / norm for x in vec]

@dataclass
class DocChunk:
    doc_id: str
    chunk_id: int
    text: str
    vector: list[float]

class DocMatch(BaseModel):
    doc_id: str
    chunk_id: int
    score: float
    text: str

def _dot(a: list[float], b: list[float]) -> float:
    return sum(x * y for x, y in zip(a, b))

def build_chunks(docs: list[dict]) -> list[DocChunk]:
    # one chunk per doc for simplicity
    out = []
    for i, d in enumerate(docs):
        out.append(
            DocChunk(
                doc_id=d["doc_id"],
                chunk_id=0,
                text=d["text"],
                vector=_embed(d["text"]),
            )
        )
    return out

def search_chunks(chunks: list[DocChunk], query: str, top_k: int = 3) -> list[DocMatch]:
    q_vec = _embed(query)
    scored: list[DocMatch] = []
    for ch in chunks:
        score = _dot(q_vec, ch.vector)
        scored.append(DocMatch(doc_id=ch.doc_id, chunk_id=ch.chunk_id, score=score, text=ch.text))
    scored.sort(key=lambda m: (-m.score, m.doc_id, m.chunk_id))
    return scored[:top_k]

# IMPORTANT: rebuild chunks AFTER defining _embed
chunks = build_chunks(docs)

preview = search_chunks(chunks, "How do I download invoices?")
print("Preview matches:")
for m in preview:
    print(m.doc_id, "score=", round(m.score, 4))

# %% [markdown]
# ### What happened (and why it matters)
# 
# - We represent each document chunk as a vector and compute similarity with a query vector using dot product.
# - `search_chunks(...)` ranks chunks by similarity and returns the top matches.
# 
# ### Why this helps the PydanticAI example
# 
# This retrieval step is what grounds the agent in factual context.  
# Next, we expose retrieval as a **PydanticAI tool**, so the agent can call it when answering and then return a structured response with citations.

# %% [markdown]
# ## Build the PydanticAI agent
# 
# Wire tools, dependencies, and a result validator into one agent.
# 
# We include two tools and a result validator that enforces basic grounding rules.
# 

# %%
from dataclasses import dataclass
from pydantic import BaseModel
from pydantic_ai import Agent, RunContext, ModelRetry
from typing import List

@dataclass
class DocDeps:
    chunks: list[dict]

class SourceRef(BaseModel):
    doc_id: str
    quote: str

class AnswerWithSources(BaseModel):
    answer: str
    sources: List[SourceRef]

# %%
def search_docs(ctx: RunContext[DocDeps], query: str, k: int = 3) -> list[dict]:
    # 1. Tokenize the user query into a set
    q_tokens = set(tokenize(query)) 
    scored = []
    
    for ch in ctx.deps.chunks:
        # 2. Check what attributes ch actually has. 
        # Replace 'content' with whatever field holds your text (e.g., 'text' or 'body')
        chunk_text = getattr(ch, 'content', '') 
        
        # 3. Tokenize the chunk text for comparison
        ch_tokens = set(tokenize(chunk_text))
        
        # 4. Calculate overlap
        overlap = len(q_tokens & ch_tokens)
        scored.append((overlap, ch))
    
    scored.sort(key=lambda x: x[0], reverse=True)
    
    # Return a list of dicts so the LLM can easily read them
    return [
        {"doc_id": c.doc_id, "content": c.content} 
        for s, c in scored[:k] if s > 0
    ]

# %%
import os

MODEL_ID = os.getenv("PYDANTIC_AI_MODEL", "openai:gpt-4o-mini")

agent = Agent(
    MODEL_ID,
    deps_type=DocDeps,
    tools=[search_docs],
    output_type=AnswerWithSources,
    instructions=(
        "You are a support assistant. "
        "Use `search_docs` to find relevant policy text. "
        "Answer briefly and include 1-3 sources with short quotes from the retrieved text."
    ),
)

@agent.output_validator
def enforce_sources(result: AnswerWithSources) -> AnswerWithSources:
    # If the answer looks like it used retrieved content, enforce citations
    keywords = ["according", "document", "policy", "invoice", "refund", "billing", "support"]
    mentions_docs = any(k in result.answer.lower() for k in keywords)

    if mentions_docs and not result.sources:
        raise ModelRetry("You referenced policies/docs but did not include sources.")

    if len(result.sources) > 3:
        raise ModelRetry("Too many sources. Maximum is 3.")

    seen = set()
    for s in result.sources:
        key = (s.doc_id, s.quote)
        if key in seen:
            raise ModelRetry("Duplicate sources. Keep sources unique.")
        seen.add(key)

    return result

# %% [markdown]
# ## Query the chatbot
# 
# Ask a question and inspect the structured response.
# 

# %%
async def ask(query: str, k: int = 3):
    deps = DocDeps(chunks=chunks)
    res = await agent.run(query, deps=deps)
    return res.output

out = await ask("How do I download my invoice?")
out

# %%
print("Answer:\n", out.answer)
print("\nSources:")
for s in out.sources:
    print(f"- {s.doc_id}: {s.quote}")

# %%
try:
    enforce_sources(AnswerWithSources(answer="According to the policy...", sources=[]))
except Exception as e:
    print("Validator failure example:", e)

# %% [markdown]
# ### What happened (and why PydanticAI helps)
# 
# This shows the validator catching an invalid output.
# In a real run, `ModelRetry` tells PydanticAI to retry until the output meets the citation rules.

# %% [markdown]
# ## Optional streaming demo
# 
# Stream a short response, then show the final validated output.
# 
# We stream a short response, then show the final structured result.
# 

# %%
# Run this cell
if not PYDANTIC_AI_AVAILABLE:
    print("Skipping: pydantic-ai not available.")
elif not _llm_ready(MODEL_ID):
    print("Skipping: API key not set for", MODEL_ID)
elif not hasattr(agent, "run_stream"):
    print("Streaming not available in this version; skipping.")
else:
    deps = DocDeps(chunks=chunks)
    async with agent.run_stream("What is the Team plan price?", deps=deps) as stream:
        print("Streaming:")
        async for chunk in stream.stream_text():
            print(chunk, end="", flush=True)
        print("\n---")
        final = await stream.get_final_result()
        _maybe_validate(final.output, deps)
        print(final.output)


# %% [markdown]
# ## Conversation memory (multi-turn)
# 
# Reuse message history to keep context across turns.
# 

# %%
# Run this cell
if not PYDANTIC_AI_AVAILABLE:
    print("Skipping: pydantic-ai not available.")
elif not _llm_ready(MODEL_ID):
    print("Skipping: API key not set for", MODEL_ID)
else:
    deps = DocDeps(chunks=chunks)
    first = await agent.run("Where do I enable 2FA?", deps=deps)
    _maybe_validate(first.output, deps)
    follow_up = await agent.run(
        "Does that work on the Starter plan?",
        deps=deps,
        message_history=first.new_messages(),
    )
    _maybe_validate(follow_up.output, deps)
    print(follow_up.output)


# %% [markdown]
# ## Guardrails (lightweight)
# 
# Reject out-of-scope questions without calling the model.
# 

# %%
# Run this cell
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


async def run_guarded(question: str, deps: DocDeps, history=None):
    if not in_scope(question):
        return AnswerWithSources(
            answer="I can only help with Atlas product documentation and support questions.",
            sources=[],
            follow_up_questions=["Do you have a question about Atlas setup, billing, or support?"],
        )
    result = await agent.run(question, deps=deps, message_history=history)
    return result.output


if not PYDANTIC_AI_AVAILABLE:
    print("Skipping: pydantic-ai not available.")
elif not _llm_ready(MODEL_ID):
    print("Skipping: API key not set for", MODEL_ID)
else:
    guarded = await run_guarded("Write me a poem about the ocean.", DocDeps(chunks=chunks))
    print(guarded)


# %% [markdown]
# ## Dynamic updates
# 
# Add new docs, rebuild the index, and query again.
# 

# %%
# Run this cell
new_doc = DOCS_DIR / "integrations.md"
if not new_doc.exists():
    new_doc.write_text(
        '''
# Integrations

Atlas supports S3 and Google Cloud Storage as data sources.
SFTP sources are available on Enterprise plans.
'''.strip() + "\n"
    )

docs = load_docs(DOCS_DIR)
chunks = build_chunks(docs)

if not PYDANTIC_AI_AVAILABLE:
    print("Skipping: pydantic-ai not available.")
elif not _llm_ready(MODEL_ID):
    print("Skipping: API key not set for", MODEL_ID)
else:
    deps = DocDeps(chunks=chunks)
    result = await agent.run("Do you support S3?", deps=deps)
    _maybe_validate(result.output, deps)
    print(result.output)


# %% [markdown]
# ## Personalization
# 
# Inject user context via dependencies to tailor responses.
# 

# %%
# Run this cell
if not PYDANTIC_AI_AVAILABLE:
    print("Skipping: pydantic-ai not available.")
elif not _llm_ready(MODEL_ID):
    print("Skipping: API key not set for", MODEL_ID)
else:
    profile = UserProfile(name="Jordan", tone="friendly", plan="Team")
    deps = DocDeps(chunks=chunks, user=profile)
    result = await agent.run("Can I enable 2FA on my plan?", deps=deps)
    _maybe_validate(result.output, deps)
    print(result.output)


# %% [markdown]
# ## What you learned
# 
# A quick recap of the core patterns you used.
# - How to build a small docs corpus and retrieve relevant snippets.
# - How to wire tools, dependencies, and result validators in a PydanticAI agent.
# - How to add memory, guardrails, and optional streaming.
# 


