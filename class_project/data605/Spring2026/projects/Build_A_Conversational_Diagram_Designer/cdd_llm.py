# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
# ---

# %% [markdown]
# # CDD LLM Client
#
# Unified interface to text-only and multimodal LLM calls.
# Default provider: Gemini 2.5 Flash (multimodal in a single model).
# Alternates: OpenAI (gpt-4o family), Anthropic (claude family).
#
# Includes automatic retry-and-backoff on 429 rate-limit errors so the
# eval harness can run safely on Gemini's free tier (5 req/min).

# %%
import json
import re
import time
from typing import Optional

import cdd_config as config


# %% [markdown]
# ## Rate-limit retry helper
#
# Gemini's free tier limits to 5 requests/minute. When we hit the limit, the
# API returns a 429 with a retry-after hint. We catch that, wait the suggested
# delay (capped to 90 seconds), and retry up to 3 times. After that we let the
# error propagate so the caller can record the failure honestly.

# %%
def _retry_on_rate_limit(fn, max_attempts=3):
    """Run `fn`, retrying on Gemini 429s with exponential backoff."""
    for attempt in range(max_attempts):
        try:
            return fn()
        except Exception as e:
            err_text = str(e)
            is_rate_limit = (
                "429" in err_text
                or "RESOURCE_EXHAUSTED" in err_text
                or "rate" in err_text.lower()
            )
            if not is_rate_limit or attempt == max_attempts - 1:
                raise
            # Try to parse the suggested retry delay; default to 30s, cap at 90s.
            wait = 30
            m = re.search(r"retry in (\d+(?:\.\d+)?)", err_text)
            if m:
                wait = min(int(float(m.group(1))) + 2, 90)
            else:
                wait = min(30 * (2 ** attempt), 90)
            print(f"[rate-limit] hit on attempt {attempt + 1}, waiting {wait}s...")
            time.sleep(wait)
    return None


# %% [markdown]
# ## Code extraction
#
# LLM responses sometimes include markdown fences or stray prose despite
# the system prompt. Pull the diagram code out cleanly.

# %%
def _extract_code(response_text: str, format: str) -> str:
    """Extract diagram code from LLM response, handling markdown fences."""
    fence_patterns = {
        "graphviz": r"```(?:dot|graphviz)?\s*\n?(.*?)```",
        "mermaid": r"```(?:mermaid)?\s*\n?(.*?)```",
        "plantuml": r"```(?:plantuml|puml|uml)?\s*\n?(.*?)```",
    }
    pattern = fence_patterns.get(format, r"```\w*\s*\n?(.*?)```")
    match = re.search(pattern, response_text, re.DOTALL)
    if match:
        return match.group(1).strip()

    stripped = response_text.strip()
    if format == "graphviz" and stripped.startswith(("digraph", "graph", "strict")):
        return stripped
    if format == "mermaid":
        first_line = stripped.split("\n", 1)[0]
        mermaid_starts = (
            "graph", "flowchart", "sequenceDiagram", "classDiagram",
            "stateDiagram", "erDiagram", "gantt", "pie", "journey",
            "gitGraph", "mindmap", "timeline",
        )
        if any(first_line.startswith(s) for s in mermaid_starts):
            return stripped
    if format == "plantuml" and "@startuml" in stripped:
        m = re.search(r"@startuml.*?@enduml", stripped, re.DOTALL)
        if m:
            return m.group(0)

    return stripped


# Backwards-compatible alias for the original tests
def _extract_dot_code(response_text: str) -> str:
    """Legacy alias - extracts DOT code. Kept for test compatibility."""
    return _extract_code(response_text, "graphviz")


# %% [markdown]
# ## Provider implementations
#
# Each provider implements two methods: generate (text-only) and critique
# (multimodal - image + text). All return a string response; the caller
# decides what to do with it.
#
# Gemini calls are wrapped in _retry_on_rate_limit so free-tier users get
# automatic backoff on 429s instead of cascading failures.

# %%
def _call_gemini(
    user_message: str,
    system_prompt: str,
    conversation_history: Optional[list] = None,
) -> str:
    """Call Gemini for text generation, with rate-limit retry."""
    from google import genai
    from google.genai import types

    def _do_call():
        client = genai.Client(api_key=config.GEMINI_API_KEY)
        contents = []
        if conversation_history:
            for msg in conversation_history:
                role = "user" if msg["role"] == "user" else "model"
                contents.append(types.Content(
                    role=role, parts=[types.Part.from_text(text=msg["content"])]
                ))
        contents.append(types.Content(
            role="user", parts=[types.Part.from_text(text=user_message)]
        ))
        response = client.models.generate_content(
            model=config.GEMINI_MODEL,
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                temperature=0.3,
            ),
        )
        return response.text or ""

    return _retry_on_rate_limit(_do_call)


def _call_gemini_vision(
    image_bytes: bytes,
    prompt: str,
    image_mime: str = "image/png",
) -> str:
    """Call Gemini multimodal: image + text prompt -> text response."""
    from google import genai
    from google.genai import types

    def _do_call():
        client = genai.Client(api_key=config.GEMINI_API_KEY)
        response = client.models.generate_content(
            model=config.GEMINI_MODEL,
            contents=[
                types.Part.from_bytes(data=image_bytes, mime_type=image_mime),
                prompt,
            ],
            config=types.GenerateContentConfig(temperature=0.2),
        )
        return response.text or ""

    return _retry_on_rate_limit(_do_call)


# %%
def _call_openai(
    user_message: str,
    system_prompt: str,
    conversation_history: Optional[list] = None,
) -> str:
    """Call OpenAI for text generation."""
    import openai
    client = openai.OpenAI(api_key=config.OPENAI_API_KEY)
    messages = [{"role": "system", "content": system_prompt}]
    if conversation_history:
        messages.extend(conversation_history)
    messages.append({"role": "user", "content": user_message})

    response = client.chat.completions.create(
        model=config.OPENAI_MODEL,
        messages=messages,
        temperature=0.3,
    )
    return response.choices[0].message.content or ""


def _call_openai_vision(
    image_bytes: bytes,
    prompt: str,
    image_mime: str = "image/png",
) -> str:
    """Call OpenAI multimodal."""
    import base64
    import openai
    client = openai.OpenAI(api_key=config.OPENAI_API_KEY)
    b64 = base64.b64encode(image_bytes).decode("utf-8")
    response = client.chat.completions.create(
        model=config.OPENAI_MODEL,
        messages=[{
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url",
                 "image_url": {"url": f"data:{image_mime};base64,{b64}"}},
            ],
        }],
        temperature=0.2,
    )
    return response.choices[0].message.content or ""


# %%
def _call_anthropic(
    user_message: str,
    system_prompt: str,
    conversation_history: Optional[list] = None,
) -> str:
    """Call Anthropic for text generation."""
    import anthropic
    client = anthropic.Anthropic(api_key=config.ANTHROPIC_API_KEY)
    messages = []
    if conversation_history:
        messages.extend(conversation_history)
    messages.append({"role": "user", "content": user_message})

    response = client.messages.create(
        model=config.ANTHROPIC_MODEL,
        max_tokens=2048,
        system=system_prompt,
        messages=messages,
        temperature=0.3,
    )
    return response.content[0].text


def _call_anthropic_vision(
    image_bytes: bytes,
    prompt: str,
    image_mime: str = "image/png",
) -> str:
    """Call Anthropic multimodal."""
    import base64
    import anthropic
    client = anthropic.Anthropic(api_key=config.ANTHROPIC_API_KEY)
    b64 = base64.b64encode(image_bytes).decode("utf-8")
    response = client.messages.create(
        model=config.ANTHROPIC_MODEL,
        max_tokens=2048,
        messages=[{
            "role": "user",
            "content": [
                {"type": "image", "source": {
                    "type": "base64", "media_type": image_mime, "data": b64,
                }},
                {"type": "text", "text": prompt},
            ],
        }],
        temperature=0.2,
    )
    return response.content[0].text


# %% [markdown]
# ## Public interface

# %%
def generate(
    user_message: str,
    format: str = "graphviz",
    conversation_history: Optional[list] = None,
    provider: Optional[str] = None,
) -> str:
    """Generate diagram code for the given format from a natural-language prompt.

    Returns the extracted code (markdown fences and prose stripped).
    """
    provider = provider or config.LLM_PROVIDER
    if format not in config.SUPPORTED_FORMATS:
        raise ValueError(f"Unsupported format: {format}. "
                         f"Choose from {config.SUPPORTED_FORMATS}.")

    system_prompt = config.SYSTEM_PROMPTS[format]

    if provider == "gemini":
        raw = _call_gemini(user_message, system_prompt, conversation_history)
    elif provider == "openai":
        raw = _call_openai(user_message, system_prompt, conversation_history)
    elif provider == "anthropic":
        raw = _call_anthropic(user_message, system_prompt, conversation_history)
    else:
        raise ValueError(f"Unknown provider: {provider}")

    return _extract_code(raw, format)


def critique_image(
    image_bytes: bytes,
    user_intent: str,
    diagram_code: str,
    provider: Optional[str] = None,
) -> dict:
    """Send a rendered diagram image to a multimodal LLM and ask for a critique.

    Returns a dict with keys: is_acceptable (bool), issues (list[str]),
    suggested_changes (str). On parse failure, returns is_acceptable=True
    so the loop terminates rather than spinning.
    """
    provider = provider or config.LLM_PROVIDER
    prompt = config.VISION_CRITIQUE_PROMPT.format(
        intent=user_intent, code=diagram_code,
    )

    if provider == "gemini":
        raw = _call_gemini_vision(image_bytes, prompt)
    elif provider == "openai":
        raw = _call_openai_vision(image_bytes, prompt)
    elif provider == "anthropic":
        raw = _call_anthropic_vision(image_bytes, prompt)
    else:
        raise ValueError(f"Unknown provider: {provider}")

    return _parse_critique(raw)


def _parse_critique(text: str) -> dict:
    """Parse a critique JSON response. Defensive against fences and prose."""
    cleaned = re.sub(r"```(?:json)?\s*", "", text).replace("```", "").strip()
    match = re.search(r"\{.*\}", cleaned, re.DOTALL)
    if match:
        try:
            data = json.loads(match.group())
            return {
                "is_acceptable": bool(data.get("is_acceptable", True)),
                "issues": list(data.get("issues", [])),
                "suggested_changes": str(data.get("suggested_changes", "")),
            }
        except (json.JSONDecodeError, ValueError):
            pass
    return {
        "is_acceptable": True,
        "issues": [],
        "suggested_changes": "",
    }


# %% [markdown]
# ## Backwards-compatible wrappers

# %%
def generate_dot(
    user_message: str,
    conversation_history: Optional[list] = None,
    provider: Optional[str] = None,
) -> str:
    """Legacy wrapper - generates Graphviz DOT specifically."""
    return generate(
        user_message,
        format="graphviz",
        conversation_history=conversation_history,
        provider=provider,
    )


def call_openai(user_message, conversation_history=None):
    """Legacy wrapper preserved for backwards compatibility."""
    return generate(user_message, "graphviz", conversation_history, provider="openai")


def call_anthropic(user_message, conversation_history=None):
    """Legacy wrapper preserved for backwards compatibility."""
    return generate(user_message, "graphviz", conversation_history, provider="anthropic")
