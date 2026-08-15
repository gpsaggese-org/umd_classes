# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.16.4
#   kernelspec:
#     display_name: .venv (3.13.7)
#     language: python
#     name: python3
# ---

# %% [markdown]
# # DocsGPT API Overview
#
# This notebook walks through every DocsGPT Cloud API endpoint one by one.
# Each section shows the raw HTTP request first, then the same call using the
# `docsgpt_utils` wrapper so you can see what the wrapper is doing under the hood.
#
# **Endpoints covered:**
#
# | Method | Endpoint | Purpose |
# |--------|----------|---------|
# | `POST` | `/api/answer` | Send a question, get a full JSON response |
# | `POST` | `/stream` | Send a question, receive the answer token by token |
# | `POST` | `/api/store_attachment` | Upload a file so the agent can read it |
# | `GET` | `/api/task_status?task_id=...` | Check whether the file upload has finished |
#
# **Setup:**
# ```bash
# ./docker_build.sh
# ./docker_jupyter.sh
# # Set your agent key before running:
# cp .env.example .env
# # Open .env and set DOCSGPT_API_KEY=your-agent-key
# ```
#
# > Get your key at https://app.docsgpt.cloud → Settings → Agents → Create New → copy the Key field.
#

# %%
# %load_ext autoreload
# %autoreload 2

import json
import logging
import os
import tempfile

import requests
import docsgpt_utils as tdgputi

from dotenv import load_dotenv
load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
_LOG = logging.getLogger(__name__)

BASE_URL = tdgputi.get_base_url()
API_KEY  = tdgputi.get_api_key()

print(f"Base URL : {BASE_URL}")
print(f"API key  : {API_KEY[:10]}***")
print("Ready ✓")

# %% [markdown]
# ---
#
# ## Endpoint 1: `POST /api/answer`
#
# `/api/answer` is the main endpoint for asking questions. You send it a JSON
# body with your question and API key. DocsGPT looks up relevant content from
# the agent's document index, passes it to the language model, and returns the
# complete answer in one JSON response — you wait for the whole thing before
# getting anything back.
#
# **Request body:**
# ```json
# {
#   "question": "Your question here",
#   "api_key":  "your-agent-key"
# }
# ```
#
# **Response fields:**
# ```json
# {
#   "answer":          "The full answer text",
#   "sources":         [{"title": "...", "text": "..."}],
#   "conversation_id": "abc123",
#   "thought":         "agent reasoning steps (if enabled)",
#   "tool_calls":      []
# }
# ```
#
# The cell below makes a raw `requests.post()` call so you can see the exact
# response shape. The cell after that makes the same call using `query_docsgpt()`.
#

# %%
# ── Raw request — see exactly what /api/answer returns ─────────────────────
question = "What is Python and what is it mainly used for?"

print(f"Request:")
print(f"  POST {BASE_URL}/api/answer")
print(f"  {{question: '{question}', api_key: '...'}}")
print()

raw_resp = requests.post(
    f"{BASE_URL}/api/answer",
    json={"question": question, "api_key": API_KEY},
    timeout=60,
)

print(f"Status       : {raw_resp.status_code}")
data = raw_resp.json()
print(f"Response keys: {list(data.keys())}")
print(f"\nanswer         : {data.get('answer', '')[:300]}")
print(f"sources        : {len(data.get('sources', []))} source(s)")
print(f"conversation_id: {data.get('conversation_id', '(none)')}")
print(f"thought        : {str(data.get('thought', '(none)'))[:100]}")

# %%
# ── Using the utility wrapper ───────────────────────────────────────────────
# query_docsgpt() is the same call, with error handling and logging built in.
result = tdgputi.query_docsgpt(question, API_KEY, BASE_URL)
tdgputi.print_answer(result, label="/api/answer")

# %% [markdown]
# ---
#
# ## Endpoint 1b: `POST /api/answer` with `history` — Multi-Turn Conversations
#
# By default, each call to `/api/answer` is independent — DocsGPT does not
# remember what was said before. To make it answer follow-up questions in
# context, you pass a `history` field containing the previous turns.
#
# **How the history field works:**
# - It is a list of past turns, where each turn has the question under `"prompt"`
#   and the answer under `"response"`
# - It must be sent as a **JSON-encoded string** (not a raw Python list) —
#   so you wrap it with `json.dumps(...)` before putting it in the payload
#
# ```python
# # Correct format
# history = json.dumps([{"prompt": "What is Python?", "response": "Python is..."}])
# ```
#
# The first cell below builds the history manually so you can see exactly what
# gets sent. The second cell uses `multi_turn_conversation()`, which does this
# automatically across any number of turns.
#

# %%
# ── Manual multi-turn to show history construction explicitly ──────────────

# Turn 1
q1 = "What is Python?"
r1 = requests.post(
    f"{BASE_URL}/api/answer",
    json={"question": q1, "api_key": API_KEY},
    timeout=60,
).json()
a1 = r1.get("answer", "")

print(f"Turn 1 Q: {q1}")
print(f"Turn 1 A: {a1[:200]}...")

# Build history in the CORRECT format
history = json.dumps([{"prompt": q1, "response": a1}])   # ← "response", not "answer"
print(f"\nHistory passed as JSON string:")
print(f"  {history[:120]}...")

# Turn 2 — follow-up question with history attached
q2 = "What are its main use cases?"
r2 = requests.post(
    f"{BASE_URL}/api/answer",
    json={"question": q2, "api_key": API_KEY, "history": history},
    timeout=60,
).json()
a2 = r2.get("answer", "")

print(f"\nTurn 2 Q: {q2}")
print(f"Turn 2 A: {a2[:200]}...")

# %%
# ── Using the wrapper — history is managed automatically ───────────────────
turns = tdgputi.multi_turn_conversation(
    [
        "What is Python?",
        "What are its main use cases?",
        "How does it compare to Java for those use cases?",
    ],
    API_KEY,
    BASE_URL,
)

for i, turn in enumerate(turns, 1):
    print(f"\n--- Turn {i} ---")
    print(f"Q: {turn['question']}")
    print(f"A: {turn['answer'][:300]}{'...' if len(turn['answer']) > 300 else ''}")

# %% [markdown]
# ---
#
# ## Endpoint 2: `POST /stream` — Streaming Responses
#
# `/stream` works like `/api/answer` but instead of waiting for the full answer,
# it sends back small pieces of text as the model generates them. This is called
# **Server-Sent Events (SSE)** — the server keeps the connection open and pushes
# data line by line.
#
# Each line that comes back starts with `data:` followed by a JSON object.
# That JSON object always has a `"type"` field that tells you what kind of
# message it is:
#
# | `type` | What it contains |
# |--------|------------------|
# | `"answer"` | One chunk of the answer text, in the `"answer"` field |
# | `"source"` | The document chunks the agent used to answer |
# | `"thought"` | The agent's reasoning steps (if your agent has this enabled) |
# | `"id"` | The conversation ID, sent at the very end |
# | `"end"` | Signals that the stream is finished |
# | `"error"` | An error message |
#
# The first cell below reads the raw SSE stream line by line so you can see
# every event. The second uses `stream_docsgpt()` which handles the parsing
# and returns the assembled answer string. The third uses
# `stream_docsgpt_events()` which yields every event dict if you need to
# access sources or the conversation ID.
#

# %%
# ── Raw SSE streaming — annotated to show every line ──────────────────────
stream_q = "What programming paradigms does Python support? Give a one-line example of each."

print(f"Request:")
print(f"  POST {BASE_URL}/stream")
print(f"  Accept: text/event-stream")
print(f"  {{question: '{stream_q[:60]}...'}}")
print("\n⚡ Live SSE events:")
print("-" * 55)

event_log: list = []

with requests.post(
    f"{BASE_URL}/stream",
    json={"question": stream_q, "api_key": API_KEY},
    stream=True,
    timeout=120,
    headers={"Accept": "text/event-stream"},
) as resp:
    resp.raise_for_status()
    for raw in resp.iter_lines():
        if not raw:
            continue
        line = raw.decode("utf-8") if isinstance(raw, bytes) else raw
        if not line.startswith("data:"):
            continue
        try:
            event = json.loads(line[5:].strip())
            event_log.append(event)
            etype = event.get("type", "?")
            if etype == "answer":
                print(event["answer"], end="", flush=True)  # ← field is "answer"
            elif etype == "end":
                print("\n[END]")
                break
            elif etype == "source":
                print(f"\n[SOURCE event — {len(event.get('sources',[]))} source(s)]")
            elif etype == "id":
                print(f"\n[ID event — conversation_id: {event.get('id', '')}]")
            elif etype == "error":
                print(f"\n[ERROR: {event.get('error', '')}]")
        except json.JSONDecodeError:
            pass

print("-" * 55)
type_counts = {}
for e in event_log:
    t = e.get("type", "?")
    type_counts[t] = type_counts.get(t, 0) + 1
print(f"\nEvent type breakdown: {type_counts}")

# %%
# ── stream_docsgpt() wrapper ───────────────────────────────────────────────
# Handles all the SSE parsing and returns the full assembled answer string.
print("Using stream_docsgpt() wrapper:")
print("-" * 55)

answer = tdgputi.stream_docsgpt(
    "What is the GIL in Python and why does it matter?",
    API_KEY,
    BASE_URL,
    print_live=True,
)
print("-" * 55)
print(f"Total chars assembled: {len(answer)}")

# %%
# ── stream_docsgpt_events() — get every event type, not just tokens ────────
# Useful when you need the sources the RAG retrieved, or the conversation ID.
print("Using stream_docsgpt_events() to capture all event types:\n")

answer_parts = []
sources      = []
conv_id      = ""

for event in tdgputi.stream_docsgpt_events(
    "Name three popular Python web frameworks.",
    API_KEY, BASE_URL,
):
    etype = event.get("type")
    if etype == "answer":
        answer_parts.append(event.get("answer", ""))
    elif etype == "source":
        sources = event.get("sources", [])
        print(f"→ Received {len(sources)} source(s) from RAG retrieval")
    elif etype == "id":
        conv_id = event.get("id", "")
        print(f"→ Conversation ID: {conv_id}")
    elif etype == "end":
        print(f"→ Stream ended")

print(f"\nFull answer: {''.join(answer_parts)[:300]}")

# %% [markdown]
# ---
#
# ## Endpoints 3 & 4: File Attachment Flow
#
# DocsGPT processes uploaded files in the background, so attaching a file
# to a query takes three separate steps:
#
# **Step 1 — Upload the file** (`POST /api/store_attachment`)
# Send the file as multipart form data. The server queues it for processing
# and immediately returns a `task_id`.
#
# **Step 2 — Wait for processing** (`GET /api/task_status?task_id=...`)
# Poll this endpoint every few seconds. When `status` becomes `"SUCCESS"`,
# the response includes an `attachment_id`.
#
# **Step 3 — Use the attachment** (`POST /stream`)
# Pass the `attachment_id` in the `"attachments"` list. The model can now
# read the file when generating its answer.
#
# ```
# POST /api/store_attachment  →  { task_id: "abc" }
#         ↓
# GET  /api/task_status       →  { status: "SUCCESS", attachment_id: "xyz" }
#         ↓
# POST /stream  (attachments: ["xyz"])  →  answer stream
# ```
#
# The three cells below go through each step. `upload_and_attach()` combines
# steps 1 and 2 into a single function call.
#

# %%
# ── Step 1: POST /api/store_attachment ────────────────────────────────────
attach_content = (
    "Transformers: A Neural Network Architecture\n\n"
    "Introduced in 'Attention is All You Need' (Vaswani et al. 2017).\n"
    "Key innovation: self-attention allows parallel processing of sequences.\n\n"
    "Core components:\n"
    "  1. Multi-head self-attention — attends to all positions simultaneously\n"
    "  2. Positional encoding       — injects sequence order without recurrence\n"
    "  3. Feed-forward layers       — applies non-linear transformations\n\n"
    "Famous models: BERT (encoder-only), GPT (decoder-only), T5 (encoder-decoder)."
)

with tempfile.NamedTemporaryFile(
    mode="w", suffix=".txt", prefix="api_test_",
    delete=False, encoding="utf-8",
) as tmp:
    tmp.write(attach_content)
    tmp_path = tmp.name

print(f"📁 Temp file  : {tmp_path}")
print(f"   Content    : {len(attach_content)} chars")
print()
print(f"Request:")
print(f"  POST {BASE_URL}/api/store_attachment")
print(f"  multipart/form-data: file=<bytes>, api_key=<key>")
print()

with open(tmp_path, "rb") as fh:
    upload_resp = requests.post(
        f"{BASE_URL}/api/store_attachment",
        files={"file": (os.path.basename(tmp_path), fh)},
        data={"api_key": API_KEY},
        timeout=60,
    )

print(f"Status   : {upload_resp.status_code}")
upload_data = upload_resp.json()
print(f"Response : {upload_data}")
task_id = upload_data.get("task_id", "")
print(f"task_id  : {task_id}")

# %%
# ── Step 2: GET /api/task_status — poll until SUCCESS ─────────────────────
print(f"Request:")
print(f"  GET {BASE_URL}/api/task_status?task_id={task_id}")
print()

attachment_id = ""

if task_id:
    # Show one raw poll to see the response shape
    single_poll = requests.get(
        f"{BASE_URL}/api/task_status",
        params={"task_id": task_id},
        timeout=15,
    ).json()
    print(f"Single poll result: {single_poll}")
    print()

    # Now use the wrapper which polls automatically until SUCCESS
    print("Polling until SUCCESS...")
    try:
        attachment_id = tdgputi.poll_attachment_status(
            task_id, BASE_URL, timeout_sec=90, poll_interval=3.0
        )
        print(f"✅ attachment_id: {attachment_id}")
    except (TimeoutError, RuntimeError) as e:
        print(f"⚠️  {e}")
else:
    print("No task_id available — skipping poll step.")

os.unlink(tmp_path)   # clean up temp file

# %%
# ── Step 3: POST /stream with attachments=[attachment_id] ─────────────────
if attachment_id:
    print(f"Request:")
    print(f"  POST {BASE_URL}/stream")
    print(f"  {{question: '...', api_key: '...', attachments: ['{attachment_id[:12]}...']}}")
    print()
    print("⚡ Streaming response with attachment:\n" + "-"*55)

    answer = tdgputi.stream_docsgpt(
        "What are the three core components described in this document? Explain each one.",
        API_KEY,
        BASE_URL,
        attachments=[attachment_id],
        print_live=True,
    )
    print("-"*55)
    print(f"✅ Answer: {len(answer)} chars")
else:
    print("No attachment_id — skipping. (Try again if the upload failed above.)")

# %% [markdown]
# ---
#
# ## Summarisation & FAQ — Sending Text in the Prompt
#
# Summarisation and FAQ generation do not use separate endpoints.
# Both work by embedding the document text directly inside the question
# and sending it to `/api/answer`.
#
# `summarize_document()` builds a prompt like this and sends it:
# ```
# Read the following document and write a summary in under {max_words} words.
#
# DOCUMENT:
# <your text here>
# ```
#
# `generate_faqs()` builds a prompt that asks for Q:/A: formatted pairs:
# ```
# Generate exactly {n} FAQs with answers. Use this format:
# Q: <question>
# A: <answer>
#
# DOCUMENT:
# <your text here>
# ```
#
# After DocsGPT responds, `parse_faqs()` splits the raw text on `Q:` markers
# and extracts each question-answer pair into a list of dicts.
#
# The text is auto-truncated to 4000 characters before sending to stay within
# the prompt size limit.
#

# %%
# ── Inline summarisation and FAQ demo ─────────────────────────────────────
sample_doc = (
    "Python is a high-level, interpreted programming language known for its clear "
    "syntax and readability. It supports multiple programming paradigms including "
    "procedural, object-oriented, and functional programming. Python is widely used "
    "in data science, machine learning, web development, and automation. It was "
    "created by Guido van Rossum and first released in 1991. Python has a large "
    "standard library and a vibrant open-source ecosystem. Its package manager pip "
    "provides access to hundreds of thousands of packages on PyPI."
)

# ── Summarisation ──────────────────────────────────────────────────────────
print("📝 SUMMARISATION via POST /api/answer (inline prompt)")
print("=" * 55)

summary = tdgputi.summarize_document(
    sample_doc, API_KEY, BASE_URL, max_words=80, source_label="api_walkthrough"
)
print(f"Summary ({len(summary.split())} words):\n{summary}")

# ── FAQ Generation ─────────────────────────────────────────────────────────
print("\n❓ FAQ GENERATION via POST /api/answer (inline prompt)")
print("=" * 55)

faqs = tdgputi.generate_faqs(
    sample_doc, API_KEY, BASE_URL, n_questions=3, source_label="api_walkthrough"
)
print(f"Generated {len(faqs)} FAQs:")
tdgputi.print_faqs(faqs)

# %% [markdown]
# ## Evaluation — ROUGE and BLEU
#
# We use two standard metrics to measure how well the generated summaries and
# FAQs capture the content of the original document.
#
# **ROUGE** (Recall-Oriented Understudy for Gisting Evaluation) counts how many
# words or phrases from the reference text appear in the generated output.
# We compute three variants:
#
# - **ROUGE-1** — counts single word matches. If the reference says
#   "machine learning" and the summary says "machine learning", both words count.
# - **ROUGE-2** — counts two-word phrase matches. "machine learning" as a pair
#   has to appear in both texts to score.
# - **ROUGE-L** — finds the longest sequence of words that appear in the same
#   order in both texts, even if not consecutive.
#
# All three return an F1 score between 0 and 1. Scores between 0.2 and 0.4 are
# typical for AI-generated summaries — the model paraphrases rather than copying,
# so exact word matches will naturally be lower.
#
# **BLEU** (Bilingual Evaluation Understudy) works from the other direction — it
# checks how many words in the generated text also appear in the reference, and
# applies a penalty if the output is too short. Also 0 to 1, higher is better.
#
# `evaluate_output(hypothesis, reference)` runs both metrics and returns a single
# dict with keys `rouge1`, `rouge2`, `rougeL`, and `bleu`. `evaluate_all()` runs
# it across every dataset, using the first 500 characters of each source text as
# the reference.

# %%
# ── Evaluation ─────────────────────────────────────────────────────────────
print("\n📊 EVALUATION (ROUGE + BLEU)")
print("=" * 55)

scores = tdgputi.evaluate_output(summary, sample_doc[:500])
tdgputi.print_scores(scores, label="summary")

# %% [markdown]
# ---
#
# ## Summary
#
# | Endpoint | Method | Wrapper function |
# |----------|--------|------------------|
# | `/api/answer` | POST | `query_docsgpt()` |
# | `/api/answer` + history | POST | `multi_turn_conversation()` |
# | `/stream` | POST | `stream_docsgpt()`, `stream_docsgpt_events()` |
# | `/api/store_attachment` | POST | `store_attachment()` |
# | `/api/task_status` | GET | `poll_attachment_status()` |
#
# **Things to remember:**
# - History is a JSON-encoded string, not a raw list
# - The history reply key is `"response"`, not `"answer"`
# - SSE answer chunks have `type == "answer"` and the text is in `event["answer"]`
# - File uploads are async — always poll until SUCCESS before using the attachment
#
