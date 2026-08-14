"""
docsgpt_utils.py
================
Utility functions for DocsGPT-based documentation assistant workflows.

DocsGPT is an AI-powered RAG platform for querying and generating content
from technical documents via a REST API on https://gptcloud.arc53.com.

Verified against: https://docs.docsgpt.cloud/Agents/api  (May 2026)

API endpoints:
  POST /api/answer           - non-streaming Q&A (full JSON)
  POST /stream               - SSE streaming Q&A (token-by-token)
  POST /api/store_attachment - upload a file attachment (multipart)
  GET  /api/task_status      - poll async attachment processing

Key design decisions:
  - With an Agent API key, document sources are pre-configured in the UI.
    Summarisation and FAQ generation embed text INLINE in the prompt so the
    LLM reasons directly over the provided content.
  - File attachments use the 3-step store_attachment flow.
  - History format: [{"prompt": "...", "response": "..."}] (official docs).
  - SSE token field: {"type": "answer", "answer": "<tok>"}.

Import as:
    import docsgpt_utils as tdgputi
"""

from __future__ import annotations

import json
import logging
import os
import re
import time
from typing import Generator

import nltk
import requests

_LOG = logging.getLogger(__name__)

DEFAULT_BASE_URL = "https://gptcloud.arc53.com"


# #############################################################################
# Configuration
# #############################################################################


def get_base_url() -> str:
    """
    Return the DocsGPT base URL with no trailing slash.

    :return: Base URL string, defaulting to the cloud URL.
    """
    return os.environ.get("DOCSGPT_BASE_URL", DEFAULT_BASE_URL).rstrip("/")


def get_api_key() -> str:
    """
    Return the DocsGPT Agent API key from the DOCSGPT_API_KEY env var.

    The key must be an *Agent* key obtained from:
      https://app.docsgpt.cloud -> Settings -> Agents -> Create New -> Key field

    :return: Agent API key string.
    :raises RuntimeError: If the DOCSGPT_API_KEY env var is not set.
    """
    key = os.environ.get("DOCSGPT_API_KEY", "").strip()
    if not key:
        raise RuntimeError(
            "DOCSGPT_API_KEY is not set.\n"
            "  1. Go to https://app.docsgpt.cloud\n"
            "  2. Settings -> Agents -> Create New\n"
            "  3. Upload your documents to the agent in the UI\n"
            "  4. Copy the Key field and run:\n"
            "       export DOCSGPT_API_KEY='your-agent-key'"
        )
    return key


# #############################################################################
# Core API wrappers
# #############################################################################


def query_docsgpt(
    question: str,
    api_key: str,
    base_url: str | None = None,
    history: list | None = None,
    save_conversation: bool = False,
) -> dict:
    """
    Send a question to DocsGPT via POST /api/answer (non-streaming).

    The agent retrieves relevant chunks from its indexed documents (RAG)
    and returns a complete answer in one JSON response.

    :param question: User question or prompt string.
    :param api_key: DocsGPT Agent API key.
    :param base_url: Override base URL; defaults to cloud URL.
    :param history: Prior conversation turns as a list of dicts.
        Format: [{"prompt": "question", "response": "answer"}]
        Note: the reply key is "response", NOT "answer".
    :param save_conversation: Persist the conversation server-side.
    :return: Dict with keys: answer, sources, conversation_id, tool_calls, thought.
    """
    base_url = base_url or get_base_url()
    payload: dict = {
        "question": question,
        "api_key": api_key,
        "save_conversation": save_conversation,
    }
    if history:
        # history must be sent as a JSON-encoded string, not a raw list.
        payload["history"] = json.dumps(history)
    _LOG.info("query_docsgpt | %s", question[:100])
    resp = requests.post(f"{base_url}/api/answer", json=payload, timeout=90)
    resp.raise_for_status()
    data = resp.json()
    _LOG.info("answer received (%d chars)", len(data.get("answer", "")))
    return data


def stream_docsgpt(
    question: str,
    api_key: str,
    base_url: str | None = None,
    history: list | None = None,
    attachments: list[str] | None = None,
    print_live: bool = True,
) -> str:
    """
    Send a question to DocsGPT via POST /stream (SSE streaming).

    Assembles all answer tokens into a single string. Optionally prints
    each token to stdout as it arrives.

    SSE event types per official docs:
      "answer"  - incremental token (field: "answer", NOT "token")
      "source"  - source chunks retrieved by RAG
      "thought" - agent reasoning steps (if enabled)
      "id"      - final conversation_id
      "error"   - error message
      "end"     - stream finished

    :param question: User question string.
    :param api_key: DocsGPT Agent API key.
    :param base_url: Override base URL.
    :param history: Prior turns: [{"prompt": "...", "response": "..."}]
    :param attachments: List of attachment_id strings from store_attachment flow.
    :param print_live: If True, print each token to stdout as it arrives.
    :return: Full answer string assembled from all SSE tokens.
    """
    base_url = base_url or get_base_url()
    payload: dict = {"question": question, "api_key": api_key}
    if history:
        payload["history"] = json.dumps(history)
    if attachments:
        payload["attachments"] = attachments
    _LOG.info("stream_docsgpt | %s", question[:100])
    tokens: list[str] = []
    with requests.post(
        f"{base_url}/stream",
        json=payload,
        stream=True,
        timeout=120,
        headers={"Accept": "text/event-stream"},
    ) as resp:
        resp.raise_for_status()
        for raw in resp.iter_lines():
            if not raw:
                continue
            line: str = raw.decode("utf-8") if isinstance(raw, bytes) else raw
            if not line.startswith("data:"):
                continue
            data_str = line[5:].strip()
            try:
                event = json.loads(data_str)
            except json.JSONDecodeError:
                continue
            etype = event.get("type", "")
            if etype == "answer":
                # Official field name is "answer".
                token = event.get("answer", "")
                if token:
                    tokens.append(token)
                    if print_live:
                        print(token, end="", flush=True)
            elif etype == "end":
                break
            elif etype == "error":
                _LOG.error("stream error: %s", event.get("error", ""))
                break
    if print_live:
        print()
    answer = "".join(tokens)
    _LOG.info("stream complete (%d chars)", len(answer))
    return answer


def stream_docsgpt_events(
    question: str,
    api_key: str,
    base_url: str | None = None,
    history: list | None = None,
) -> Generator[dict, None, None]:
    """
    Send a question to DocsGPT via POST /stream and yield every raw SSE event.

    Use this when you need access to source, thought, or id events in addition
    to answer tokens. Each yielded dict has at least a 'type' key.

    :param question: User question string.
    :param api_key: DocsGPT Agent API key.
    :param base_url: Override base URL.
    :param history: Prior turns: [{"prompt": "...", "response": "..."}]
    :return: Generator of SSE event dicts.
    """
    base_url = base_url or get_base_url()
    payload: dict = {"question": question, "api_key": api_key}
    if history:
        payload["history"] = json.dumps(history)
    with requests.post(
        f"{base_url}/stream",
        json=payload,
        stream=True,
        timeout=120,
        headers={"Accept": "text/event-stream"},
    ) as resp:
        resp.raise_for_status()
        for raw in resp.iter_lines():
            if not raw:
                continue
            line: str = raw.decode("utf-8") if isinstance(raw, bytes) else raw
            if not line.startswith("data:"):
                continue
            data_str = line[5:].strip()
            try:
                event = json.loads(data_str)
                yield event
                if event.get("type") == "end":
                    break
            except json.JSONDecodeError:
                continue


def multi_turn_conversation(
    questions: list[str],
    api_key: str,
    base_url: str | None = None,
) -> list[dict]:
    """
    Run a multi-turn conversation, accumulating history between turns.

    Each turn appends to history using the official format so the agent
    has full context when answering follow-up questions.

    :param questions: Ordered list of question strings.
    :param api_key: DocsGPT Agent API key.
    :param base_url: Override base URL.
    :return: List of turn dicts, each with keys: question, answer, sources,
        conversation_id.
    """
    base_url = base_url or get_base_url()
    # History format per official docs: key is "response", not "answer".
    history: list[dict] = []
    turns: list[dict] = []
    for q in questions:
        result = query_docsgpt(q, api_key, base_url, history=history)
        answer = result.get("answer", "")
        history.append({"prompt": q, "response": answer})
        turns.append({
            "question":        q,
            "answer":          answer,
            "sources":         result.get("sources", []),
            "conversation_id": result.get("conversation_id", ""),
        })
        _LOG.info("multi-turn: turn %d complete", len(turns))
    return turns


# #############################################################################
# Attachment API  (3-step: upload -> poll -> attach to /stream)
# #############################################################################


def store_attachment(
    file_path: str,
    api_key: str,
    base_url: str | None = None,
) -> str:
    """
    Upload a file via POST /api/store_attachment and return the task_id.

    Step 1 of the attachment flow. Processing is asynchronous — call
    poll_attachment_status() after this to wait for completion.

    :param file_path: Local path to the file to upload.
    :param api_key: DocsGPT Agent API key.
    :param base_url: Override base URL.
    :return: task_id string to pass to poll_attachment_status().
    """
    base_url = base_url or get_base_url()
    _LOG.info("store_attachment: %s", file_path)
    with open(file_path, "rb") as fh:
        resp = requests.post(
            f"{base_url}/api/store_attachment",
            files={"file": (os.path.basename(file_path), fh)},
            data={"api_key": api_key},
            timeout=60,
        )
    resp.raise_for_status()
    data = resp.json()
    task_id = data.get("task_id", "")
    _LOG.info("store_attachment task_id: %s", task_id)
    return task_id


def poll_attachment_status(
    task_id: str,
    base_url: str | None = None,
    timeout_sec: int = 120,
    poll_interval: float = 3.0,
) -> str:
    """
    Poll GET /api/task_status until attachment processing succeeds.

    Step 2 of the attachment flow.

    :param task_id: Task ID returned by store_attachment().
    :param base_url: Override base URL.
    :param timeout_sec: Maximum seconds to wait before raising TimeoutError.
    :param poll_interval: Seconds to wait between polls.
    :return: attachment_id string to use in stream_docsgpt(attachments=[...]).
    :raises TimeoutError: If the task does not complete within timeout_sec.
    :raises RuntimeError: If the task fails or is revoked.
    """
    base_url = base_url or get_base_url()
    deadline = time.time() + timeout_sec
    _LOG.info("polling task_status for task_id=%s", task_id)
    while time.time() < deadline:
        resp = requests.get(
            f"{base_url}/api/task_status",
            params={"task_id": task_id},
            timeout=15,
        )
        resp.raise_for_status()
        data = resp.json()
        status = data.get("status", "")
        _LOG.debug("task status: %s", status)
        if status == "SUCCESS":
            attachment_id = data.get("result", {}).get("attachment_id", "")
            _LOG.info("attachment ready: %s", attachment_id)
            return attachment_id
        if status in ("FAILURE", "REVOKED"):
            raise RuntimeError(f"Attachment task failed: {data}")
        time.sleep(poll_interval)
    raise TimeoutError(f"Attachment task {task_id} not ready after {timeout_sec}s")


def upload_and_attach(
    file_path: str,
    api_key: str,
    base_url: str | None = None,
    timeout_sec: int = 120,
) -> str:
    """
    Upload a file and wait for its attachment_id (combines steps 1 and 2).

    :param file_path: Local path to the file to upload.
    :param api_key: DocsGPT Agent API key.
    :param base_url: Override base URL.
    :param timeout_sec: Maximum seconds to wait for processing.
    :return: attachment_id ready for stream_docsgpt(attachments=[...]).
    """
    task_id = store_attachment(file_path, api_key, base_url)
    return poll_attachment_status(task_id, base_url, timeout_sec)


# #############################################################################
# Summarisation  (inline prompt — no upload needed)
# #############################################################################


def summarize_document(
    text: str,
    api_key: str,
    base_url: str | None = None,
    max_words: int = 200,
    source_label: str = "document",
) -> str:
    """
    Summarise document text by embedding it inline in the prompt.

    Sends the text directly inside the question to POST /api/answer.
    No file upload is needed — the LLM reasons over the provided content.
    Text is auto-truncated to 4000 characters before sending.

    :param text: Plain text to summarise.
    :param api_key: DocsGPT Agent API key.
    :param base_url: Override base URL.
    :param max_words: Target word count for the summary.
    :param source_label: Label used only for logging.
    :return: Summary string from DocsGPT.
    """
    base_url = base_url or get_base_url()
    text = truncate_text(text, max_chars=4000)
    prompt = (
        f"Read the following document carefully and write a concise, well-structured "
        f"summary in no more than {max_words} words. Capture the key concepts, main "
        f"points, and important details.\n\n"
        f"DOCUMENT:\n{text}"
    )
    _LOG.info("summarize_document: '%s' (%d chars)", source_label, len(text))
    result = query_docsgpt(prompt, api_key, base_url)
    return result.get("answer", "")


# #############################################################################
# FAQ generation  (inline prompt — no upload needed)
# #############################################################################


def generate_faqs(
    text: str,
    api_key: str,
    base_url: str | None = None,
    n_questions: int = 5,
    source_label: str = "document",
) -> list[dict]:
    """
    Generate FAQ question-answer pairs from document text.

    Sends the text inline in the prompt to POST /api/answer and parses
    the Q:/A: formatted response into structured dicts.
    Text is auto-truncated to 4000 characters before sending.

    :param text: Plain text to generate FAQs from.
    :param api_key: DocsGPT Agent API key.
    :param base_url: Override base URL.
    :param n_questions: Number of FAQ items to request.
    :param source_label: Label used only for logging.
    :return: List of dicts with keys 'question' and 'answer'.
    """
    base_url = base_url or get_base_url()
    text = truncate_text(text, max_chars=4000)
    prompt = (
        f"Based on the document below, generate exactly {n_questions} frequently asked "
        f"questions (FAQs) with detailed, helpful answers.\n\n"
        f"Use this EXACT format for every FAQ (no deviation):\n"
        f"Q: <question>\n"
        f"A: <answer>\n\n"
        f"Separate each FAQ pair with a blank line.\n\n"
        f"DOCUMENT:\n{text}"
    )
    _LOG.info("generate_faqs: %d Qs for '%s'", n_questions, source_label)
    result = query_docsgpt(prompt, api_key, base_url)
    raw = result.get("answer", "")
    return parse_faqs(raw)


def parse_faqs(raw_text: str) -> list[dict]:
    """
    Parse DocsGPT FAQ output in Q:/A: format into a list of dicts.

    :param raw_text: Raw answer string from DocsGPT containing Q:/A: pairs.
    :return: List of dicts, each with keys 'question' and 'answer'.
    """
    faqs: list[dict] = []
    blocks = re.split(r"\n{1,2}(?=Q:)", raw_text.strip())
    for block in blocks:
        q_match = re.search(r"Q:\s*(.+?)(?:\n|$)", block, re.IGNORECASE)
        a_match = re.search(r"A:\s*(.+)", block, re.IGNORECASE | re.DOTALL)
        if q_match and a_match:
            faqs.append({
                "question": q_match.group(1).strip(),
                "answer":   a_match.group(1).strip(),
            })
    return faqs


# #############################################################################
# Dataset loaders
# #############################################################################


def fetch_awesome_ml_readme(
    url: str = (
        "https://raw.githubusercontent.com/josephmisiti/"
        "awesome-machine-learning/master/README.md"
    ),
) -> str:
    """
    Fetch the Awesome Machine Learning README from GitHub.

    :param url: Raw GitHub URL for the README.
    :return: Full README text as a string.
    """
    _LOG.info("fetching Awesome ML README from %s", url)
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    _LOG.info("fetched %d chars", len(resp.text))
    return resp.text


def parse_awesome_ml_sections(raw_md: str) -> dict[str, str]:
    """
    Parse the Awesome ML README into a dict of section title to body text.

    :param raw_md: Raw markdown string of the README.
    :return: Dict mapping section title string to section body string.
    """
    sections: dict[str, str] = {}
    current_title = "Preamble"
    current_lines: list[str] = []
    for line in raw_md.splitlines():
        if line.startswith("## "):
            sections[current_title] = "\n".join(current_lines).strip()
            current_title = line.lstrip("# ").strip()
            current_lines = []
        else:
            current_lines.append(line)
    sections[current_title] = "\n".join(current_lines).strip()
    _LOG.info("parsed %d sections from Awesome ML README", len(sections))
    return sections


def load_stackoverflow_sample(n_rows: int = 20) -> list[dict]:
    """
    Load Stack Overflow questions from HuggingFace Hub via streaming.

    Uses streaming so the full dataset is never downloaded. Falls back to
    a built-in synthetic sample if the dataset is unavailable.

    :param n_rows: Number of rows to load.
    :return: List of dicts with keys: title, body, answer.
    """
    try:
        from datasets import load_dataset  # type: ignore
        _LOG.info("loading SO dataset (streaming, n=%d)", n_rows)
        ds = load_dataset(
            "pacovaldez/stackoverflow-questions",
            split="train",
            streaming=True,
            trust_remote_code=True,
        )
        rows: list[dict] = []
        for i, row in enumerate(ds):
            if i >= n_rows:
                break
            rows.append({
                "title":  row.get("Title",  row.get("title",  "")),
                "body":   row.get("Body",   row.get("body",   "")),
                "answer": row.get("Answer", row.get("answer", "")),
            })
        _LOG.info("loaded %d SO rows", len(rows))
        return rows
    except Exception as exc:
        _LOG.warning("SO dataset unavailable: %s — using fallback", exc)
        return _synthetic_stackoverflow_sample(n_rows)


def _synthetic_stackoverflow_sample(n: int) -> list[dict]:
    """
    Return a built-in synthetic Stack Overflow sample for offline fallback.

    :param n: Number of rows to return.
    :return: List of dicts with keys: title, body, answer.
    """
    template = [
        {
            "title":  "How do I reverse a list in Python?",
            "body":   "I have a list and want it reversed. What is the most Pythonic way?",
            "answer": "Use list.reverse() to reverse in-place, or my_list[::-1] for a new reversed list.",
        },
        {
            "title":  "What is a Docker volume?",
            "body":   "I need to persist data across container restarts. What should I use?",
            "answer": "A Docker volume is managed storage outside the container filesystem that persists between restarts.",
        },
        {
            "title":  "Difference between supervised and unsupervised learning?",
            "body":   "What is the key difference between supervised and unsupervised ML?",
            "answer": "Supervised learning trains on labelled data. Unsupervised learning finds structure in unlabelled data.",
        },
        {
            "title":  "What is gradient descent?",
            "body":   "Explain gradient descent and how it is used in ML model training.",
            "answer": "Gradient descent minimises a loss function by iteratively updating parameters in the direction of the negative gradient.",
        },
        {
            "title":  "SQL vs NoSQL — when to use each?",
            "body":   "When should I choose a SQL database over a NoSQL one?",
            "answer": "Use SQL for structured data with complex queries. Use NoSQL for flexible schemas and high-volume unstructured data.",
        },
        {
            "title":  "What is a REST API?",
            "body":   "Can you explain what a REST API is and its core principles?",
            "answer": "REST is an architectural style over HTTP. Core principles: statelessness, uniform interface, client-server separation, cacheability.",
        },
    ]
    return [template[i % len(template)] for i in range(n)]


def load_pile_sample(n_chars: int = 8000) -> str:
    """
    Load a text sample from The Pile (uncopyrighted) via HuggingFace streaming.

    Falls back to a built-in NLP passage if the dataset is unavailable.

    :param n_chars: Approximate number of characters to collect.
    :return: Text string of approximately n_chars characters.
    """
    try:
        from datasets import load_dataset  # type: ignore
        _LOG.info("streaming Pile dataset (target %d chars)", n_chars)
        ds = load_dataset(
            "monology/pile-uncopyrighted",
            split="train",
            streaming=True,
            trust_remote_code=True,
        )
        collected: list[str] = []
        total = 0
        for row in ds:
            text = row.get("text", "")
            collected.append(text)
            total += len(text)
            if total >= n_chars:
                break
        result = "\n\n".join(collected)
        _LOG.info("collected %d chars from Pile", len(result))
        return result
    except Exception as exc:
        _LOG.warning("Pile dataset unavailable: %s — using fallback", exc)
        return (
            "Natural language processing (NLP) is a subfield of artificial intelligence "
            "that focuses on enabling computers to understand, interpret, and generate "
            "human language. Modern NLP relies on large transformer-based models such as "
            "BERT, GPT, and T5 that are pretrained on massive corpora and fine-tuned for "
            "specific tasks. Key NLP tasks include text classification, named entity "
            "recognition, sentiment analysis, machine translation, text summarisation, "
            "and question answering. The attention mechanism, introduced in 'Attention is "
            "All You Need' (Vaswani et al., 2017), allows models to weigh word importance "
            "across a sequence. Transfer learning dramatically reduced the labelled data "
            "required for downstream tasks. NLP applications power search engines, virtual "
            "assistants, chatbots, content moderation, and automated document analysis."
        )


# #############################################################################
# Text preprocessing helpers
# #############################################################################


def clean_markdown(text: str) -> str:
    """
    Strip markdown syntax to produce clean plain prose.

    Removes HTML tags, link syntax, headings, bullet points, code blocks,
    inline code, and bold/italic markers.

    :param text: Raw markdown string.
    :return: Clean plain-text string.
    """
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"^#{1,6}\s+", "", text, flags=re.MULTILINE)
    text = re.sub(r"^\s*[-*+]\s+", "", text, flags=re.MULTILINE)
    text = re.sub(r"```[^`]*```", " ", text, flags=re.DOTALL)
    text = re.sub(r"`[^`]+`", " ", text)
    text = re.sub(r"\*{1,2}([^*]+)\*{1,2}", r"\1", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"[ \t]+", " ", text)
    return text.strip()


def chunk_text(
    text: str,
    max_chars: int = 2000,
    overlap: int = 200,
) -> list[str]:
    """
    Split a long document into overlapping character-level chunks.

    :param text: Input text string.
    :param max_chars: Maximum characters per chunk.
    :param overlap: Overlap in characters between consecutive chunks.
    :return: List of text chunk strings.
    :raises ValueError: If max_chars is not greater than overlap.
    """
    if max_chars <= overlap:
        raise ValueError("max_chars must be greater than overlap")
    chunks: list[str] = []
    start = 0
    while start < len(text):
        end = min(start + max_chars, len(text))
        chunks.append(text[start:end])
        if end == len(text):
            break
        start += max_chars - overlap
    return chunks


def truncate_text(text: str, max_chars: int = 4000) -> str:
    """
    Truncate text to at most max_chars characters.

    :param text: Input text string.
    :param max_chars: Maximum number of characters to keep.
    :return: Truncated string, with '[truncated]' appended if cut.
    """
    if len(text) <= max_chars:
        return text
    return text[:max_chars].rstrip() + " [truncated]"


def so_rows_to_text(rows: list[dict]) -> str:
    """
    Convert Stack Overflow row dicts into a single plain-text document.

    :param rows: List of dicts with keys: title, body, answer.
    :return: Combined plain-text string with --- separators between rows.
    """
    parts: list[str] = []
    for row in rows:
        title  = row.get("title", "")
        body   = clean_markdown(row.get("body", ""))
        answer = clean_markdown(row.get("answer", ""))
        parts.append(f"Question: {title}\n{body}\n\nAnswer:\n{answer}")
    return "\n\n---\n\n".join(parts)


# #############################################################################
# Multi-language support
# #############################################################################


SUPPORTED_LANGUAGES: dict[str, str] = {
    "en": "English",
    "es": "Spanish",
    "fr": "French",
    "de": "German",
    "zh": "Chinese",
    "pt": "Portuguese",
    "it": "Italian",
    "ja": "Japanese",
    "ar": "Arabic",
}


def list_supported_languages() -> dict[str, str]:
    """
    Return the mapping of ISO-639-1 code to language name.

    :return: Dict of {code: language_name}.
    """
    return dict(SUPPORTED_LANGUAGES)


def translate_text(
    text: str,
    source: str = "auto",
    target: str = "en",
) -> str:
    """
    Translate text using deep-translator (Google Translate backend).

    Handles texts longer than Google's ~4500-char limit by sentence-batching:
    splits on sentence boundaries, translates each batch, then joins.

    :param text: Source text to translate.
    :param source: Source language ISO-639-1 code or 'auto' for auto-detect.
    :param target: Target language ISO-639-1 code.
    :return: Translated string.
    """
    from deep_translator import GoogleTranslator  # type: ignore
    if source == target:
        return text
    _LOG.info("translating %d chars: %s -> %s", len(text), source, target)
    max_chunk = 4500
    if len(text) <= max_chunk:
        return GoogleTranslator(source=source, target=target).translate(text) or text
    sentences = re.split(r"(?<=[.!?])\s+", text)
    batches: list[str] = []
    current: list[str] = []
    current_len = 0
    for sent in sentences:
        if current_len + len(sent) > max_chunk and current:
            batches.append(" ".join(current))
            current, current_len = [sent], len(sent)
        else:
            current.append(sent)
            current_len += len(sent)
    if current:
        batches.append(" ".join(current))
    parts = [
        GoogleTranslator(source=source, target=target).translate(b) or b
        for b in batches
    ]
    return " ".join(parts)


def summarize_multilang(
    text: str,
    api_key: str,
    source_lang: str = "en",
    output_lang: str = "es",
    base_url: str | None = None,
    max_words: int = 200,
    source_label: str = "doc",
) -> dict:
    """
    Summarise a document and return the summary in a target language.

    Pipeline: (translate to EN if needed) -> DocsGPT summarise
              -> (translate to target language).

    :param text: Input document text.
    :param api_key: DocsGPT Agent API key.
    :param source_lang: ISO-639-1 code of the input language.
    :param output_lang: ISO-639-1 code of the desired output language.
    :param base_url: Override base URL.
    :param max_words: Target word count for the summary.
    :param source_label: Label used only for logging.
    :return: Dict with keys 'english_summary' and 'translated_summary'.
    """
    base_url = base_url or get_base_url()
    english_text = (
        text if source_lang == "en"
        else translate_text(text, source_lang, "en")
    )
    english_summary = summarize_document(
        english_text, api_key, base_url, max_words, source_label
    )
    text_to_translate = clean_markdown(english_summary)
    translated = (
        english_summary if output_lang == "en"
        else translate_text(text_to_translate, "en", output_lang)
    )
    return {"english_summary": english_summary, "translated_summary": translated}


def generate_faqs_multilang(
    text: str,
    api_key: str,
    source_lang: str = "en",
    output_lang: str = "es",
    n_questions: int = 5,
    base_url: str | None = None,
    source_label: str = "doc",
) -> dict:
    """
    Generate FAQs from a document and return them in a target language.

    :param text: Input document text.
    :param api_key: DocsGPT Agent API key.
    :param source_lang: ISO-639-1 code of the input language.
    :param output_lang: ISO-639-1 code of the desired output language.
    :param n_questions: Number of FAQ items to generate.
    :param base_url: Override base URL.
    :param source_label: Label used only for logging.
    :return: Dict with keys 'english_faqs' and 'translated_faqs',
        each a list of dicts with keys 'question' and 'answer'.
    """
    base_url = base_url or get_base_url()
    english_text = (
        text if source_lang == "en"
        else translate_text(text, source_lang, "en")
    )
    english_faqs = generate_faqs(
        english_text, api_key, base_url, n_questions, source_label
    )
    if output_lang == "en":
        return {"english_faqs": english_faqs, "translated_faqs": english_faqs}
    translated_faqs = [
        {
            "question": translate_text(f["question"], "en", output_lang),
            "answer":   translate_text(f["answer"],   "en", output_lang),
        }
        for f in english_faqs
    ]
    return {"english_faqs": english_faqs, "translated_faqs": translated_faqs}


# #############################################################################
# Evaluation metrics (ROUGE + BLEU)
# #############################################################################


def rouge_scores(hypothesis: str, reference: str) -> dict[str, float]:
    """
    Compute ROUGE-1, ROUGE-2, and ROUGE-L F1 scores.

    :param hypothesis: Generated text (e.g. DocsGPT summary or FAQ answer).
    :param reference: Ground-truth reference text.
    :return: Dict with keys 'rouge1', 'rouge2', 'rougeL', all floats in [0, 1].
    """
    from rouge_score import rouge_scorer as rs  # type: ignore
    scorer = rs.RougeScorer(["rouge1", "rouge2", "rougeL"], use_stemmer=True)
    scores = scorer.score(reference, hypothesis)
    return {
        "rouge1": round(scores["rouge1"].fmeasure, 4),
        "rouge2": round(scores["rouge2"].fmeasure, 4),
        "rougeL": round(scores["rougeL"].fmeasure, 4),
    }


def bleu_score(hypothesis: str, reference: str) -> float:
    """
    Compute sentence-level BLEU score with smoothing (NLTK).

    :param hypothesis: Generated text.
    :param reference: Ground-truth reference text.
    :return: BLEU score as float in [0, 1].
    """
    from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction  # type: ignore
    nltk.download("punkt",     quiet=True)
    nltk.download("punkt_tab", quiet=True)
    ref_tokens = reference.lower().split()
    hyp_tokens = hypothesis.lower().split()
    sf = SmoothingFunction().method1
    return round(sentence_bleu([ref_tokens], hyp_tokens, smoothing_function=sf), 4)


def evaluate_output(hypothesis: str, reference: str) -> dict[str, float]:
    """
    Evaluate generated text against a reference using ROUGE and BLEU.

    :param hypothesis: Generated text.
    :param reference: Ground-truth reference text.
    :return: Dict with keys 'rouge1', 'rouge2', 'rougeL', 'bleu'.
    """
    r = rouge_scores(hypothesis, reference)
    b = bleu_score(hypothesis, reference)
    result = {**r, "bleu": b}
    _LOG.info("evaluate_output: %s", result)
    return result


def evaluate_all(
    summaries: dict[str, str],
    faqs: dict[str, list[dict]],
    source_texts: dict[str, str],
) -> dict[str, dict[str, float]]:
    """
    Evaluate summaries and FAQ answers for multiple labelled documents.

    Uses the first 500 chars of each source text as the ground-truth reference.

    :param summaries: Dict of {label: summary_string}.
    :param faqs: Dict of {label: [{"question": ..., "answer": ...}]}.
    :param source_texts: Dict of {label: full_source_text}.
    :return: Dict of {label: {rouge1, rouge2, rougeL, bleu, faq_rouge1, ...}}.
    """
    results: dict = {}
    for label in summaries:
        reference = truncate_text(source_texts.get(label, ""), max_chars=500)
        summary_scores = evaluate_output(summaries[label], reference)
        faq_list = faqs.get(label, [])
        faq_scores: dict = {}
        if faq_list:
            fs = evaluate_output(faq_list[0]["answer"], reference)
            faq_scores = {f"faq_{k}": v for k, v in fs.items()}
        results[label] = {**summary_scores, **faq_scores}
    return results


# #############################################################################
# Display helpers
# #############################################################################


def print_answer(result: dict, label: str = "") -> None:
    """
    Pretty-print a query_docsgpt() result dict.

    :param result: Dict returned by query_docsgpt().
    :param label: Optional label prefix for output lines.
    """
    prefix = f"[{label}] " if label else ""
    print(f"\n{prefix}ANSWER:\n{result.get('answer', '(no answer)')}")
    sources = result.get("sources", [])
    if sources:
        print(f"{prefix}SOURCES: {sources}")


def print_faqs(faqs: list[dict], label: str = "") -> None:
    """
    Pretty-print a list of FAQ dicts.

    :param faqs: List of dicts with keys 'question' and 'answer'.
    :param label: Optional label prefix for output lines.
    """
    prefix = f"[{label}] " if label else ""
    if not faqs:
        print(f"{prefix}(no FAQs generated)")
        return
    for i, faq in enumerate(faqs, 1):
        print(f"\n{prefix}Q{i}: {faq['question']}")
        print(f"{prefix}A{i}: {faq['answer']}")


def print_scores(scores: dict, label: str = "") -> None:
    """
    Pretty-print an evaluation score dict.

    :param scores: Dict of metric_name -> float score.
    :param label: Optional label prefix for output lines.
    """
    prefix = f"[{label}] " if label else ""
    for k, v in scores.items():
        print(f"  {prefix}{k.upper()}: {v:.4f}")
