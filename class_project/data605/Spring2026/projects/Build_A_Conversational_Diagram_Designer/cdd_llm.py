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

# %%
import json
import re
from typing import Optional

import cdd_config as config


# %% [markdown]
# ## Code extraction
#
# LLM responses sometimes include markdown fences or stray prose despite
# the system prompt. Pull the diagram code out cleanly.

# %%
def _extract_code(response_text: str, format: str) -> str:
    """Extract diagram code from LLM response, handling markdown fences."""
    # Try fenced blocks for the specific format
    fence_patterns = {
        "graphviz": r"```(?:dot|graphviz)?\s*\n?(.*?)```",
        "mermaid": r"```(?:mermaid)?\s*\n?(.*?)```",
        "plantuml": r"```(?:plantuml|puml|uml)?\s*\n?(.*?)```",
    }
    pattern = fence_patterns.get(format, r"```\w*\s*\n?(.*?)```")
    match = re.search(pattern, response_text, re.DOTALL)
    if match:
        return match.group(1).strip()

    # No fence: strip and check for known starts
    stripped = response_text.strip()
    if format == "graphviz" and stripped.startswith(("digraph", "graph", "strict")):
        return stripped
    if format == "mermaid":
        # Mermaid diagrams start with a type keyword
        first_line = stripped.split("\n", 1)[0]
        mermaid_starts = (
            "graph", "flowchart", "sequenceDiagram", "classDiagram",
            "stateDiagram", "erDiagram", "gantt", "pie", "journey",
            "gitGraph", "mindmap", "timeline",
        )
        if any(first_line.startswith(s) for s in mermaid_starts):
            return stripped
    if format == "plantuml" and "@startuml" in stripped:
        # Trim to just the @startuml ... @enduml block
        m = re.search(r"@startuml.*?@enduml", stripped, re.DOTALL)
        if m:
            return m.group(0)

    return stripped


# %% [markdown]
# ## Backwards-compatible alias for the original tests

# %%
def _extract_dot_code(response_text: str) -> str:
    """Legacy alias — extracts DOT code. Kept for test compatibility."""
    return _extract_code(response_text, "graphviz")


# %% [markdown]
# ## Provider implementations
#
# Each provider implements two methods: generate (text-only) and critique
# (multimodal — image + text). All return a string response; the caller
# decides what to do with it.

# %%
def _call_gemini(
    user_message: str,
    system_prompt: str,
    conversation_history: Optional[list] = None,
) -> str:
    """Call Gemini for text generation."""
    from google import genai
    from google.genai import types

    client = genai.Client(api_key=config.GEMINI_API_KEY)

    # Gemini takes a list of Content objects. We map our history (which uses
    # OpenAI's role/content shape) into Gemini's parts format.
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


def _call_gemini_vision(
    image_bytes: bytes,
    prompt: str,
    image_mime: str = "image/png",
) -> str:
    """Call Gemini multimodal: image + text prompt -> text response."""
    from google import genai
    from google.genai import types

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
    # Strip markdown fences if the model added them
    cleaned = re.sub(r"```(?:json)?\s*", "", text).replace("```", "").strip()
    # Find the first { ... } block
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
    # Fallback: treat as acceptable so the loop terminates safely
    return {
        "is_acceptable": True,
        "issues": [],
        "suggested_changes": "",
    }


# %% [markdown]
# ## Describe-and-suggest
#
# After the final render, send the image to a multimodal LLM and ask for a
# plain-English description plus concrete suggestions for further changes.
# This is shown in the chat alongside the diagram. Failures are non-fatal:
# if the call or parse fails we return empty fields and the UI just shows
# the diagram as before.

# %%
def describe_and_suggest(
    image_bytes: bytes,
    user_intent: str,
    diagram_code: str,
    diagram_format: str = "graphviz",
    provider: Optional[str] = None,
) -> dict:
    """Generate a description of the rendered diagram plus suggestions for
    further changes.

    Returns: {"description": str, "suggestions": list[str]}.
    On any failure returns empty fields so the caller can render gracefully.
    """
    provider = provider or config.LLM_PROVIDER
    prompt = config.DESCRIBE_SUGGEST_PROMPT.format(
        intent=user_intent or "(no specific intent recorded)",
        code=diagram_code,
        format=diagram_format,
    )

    try:
        if provider == "gemini":
            raw = _call_gemini_vision(image_bytes, prompt)
        elif provider == "openai":
            raw = _call_openai_vision(image_bytes, prompt)
        elif provider == "anthropic":
            raw = _call_anthropic_vision(image_bytes, prompt)
        else:
            raise ValueError(f"Unknown provider: {provider}")
    except Exception as e:
        # Log to stderr so you can spot failed calls in the server log.
        # The user-facing path stays graceful: empty fields, no crash.
        import sys
        print(
            f"[describe_and_suggest] LLM call failed: {e}",
            file=sys.stderr,
        )
        return {"description": "", "suggestions": []}

    parsed = _parse_describe_suggest(raw)

    # If parsing yielded nothing, log the raw response so we can diagnose
    # why Gemini's output isn't producing chat bubbles. Truncate to keep
    # logs readable.
    if not parsed["description"] and not parsed["suggestions"]:
        import sys
        snippet = (raw or "")[:500].replace("\n", " ")
        print(
            f"[describe_and_suggest] Empty parse. Raw response: {snippet!r}",
            file=sys.stderr,
        )

    return parsed


def _parse_describe_suggest(text: str) -> dict:
    """Parse the describe+suggest JSON response. Defensive against fences,
    smart quotes, trailing commas, and stray prose."""
    if not text:
        return {"description": "", "suggestions": []}

    # 1. Strip markdown fences (```json ... ``` or just ``` ... ```).
    cleaned = re.sub(r"```(?:json)?\s*", "", text).replace("```", "").strip()

    # 2. Replace common smart-quote characters with regular quotes — Gemini
    #    occasionally returns curly quotes, which json.loads can't parse.
    cleaned = (
        cleaned.replace("\u201c", '"').replace("\u201d", '"')
               .replace("\u2018", "'").replace("\u2019", "'")
    )

    # 3. Find the outermost {...} block.
    match = re.search(r"\{.*\}", cleaned, re.DOTALL)
    if not match:
        return {"description": "", "suggestions": []}

    candidate = match.group()

    # 4. Try parsing as-is first; if that fails, strip trailing commas
    #    inside arrays/objects (a common LLM mistake) and retry.
    for attempt in (candidate, re.sub(r",(\s*[}\]])", r"\1", candidate)):
        try:
            data = json.loads(attempt)
            description = str(data.get("description", "")).strip()
            raw_sugs = data.get("suggestions", [])
            # Coerce to list[str], drop empties, strip whitespace
            if isinstance(raw_sugs, str):
                raw_sugs = [raw_sugs]
            suggestions = [
                str(s).strip() for s in raw_sugs if str(s).strip()
            ]
            return {
                "description": description,
                "suggestions": suggestions,
            }
        except (json.JSONDecodeError, ValueError):
            continue

    # All parse attempts failed.
    return {"description": "", "suggestions": []}


# %% [markdown]
# ## Backwards-compatible wrappers
#
# The original tests and notebooks call `generate_dot`. Keep that name
# as a thin alias so existing code keeps working.

# %%
def generate_dot(
    user_message: str,
    conversation_history: Optional[list] = None,
    provider: Optional[str] = None,
) -> str:
    """Legacy wrapper — generates Graphviz DOT specifically."""
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