# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
# ---

# %% [markdown]
# # CDD Configuration
#
# Central configuration for the Conversational Diagram Designer.
# Holds LLM provider settings, format definitions, system prompts,
# and the vision-feedback loop parameters.

# %%
import os
from dotenv import load_dotenv

load_dotenv()

# %% [markdown]
# ## LLM provider configuration
#
# Default: Gemini 2.5 Flash (multimodal, free tier).
# OpenAI and Anthropic are supported as alternatives if their keys are set.

# %%
LLM_PROVIDER = os.getenv("CDD_LLM_PROVIDER", "gemini")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")

GEMINI_MODEL = os.getenv("CDD_GEMINI_MODEL", "gemini-2.5-flash")
OPENAI_MODEL = os.getenv("CDD_OPENAI_MODEL", "gpt-4o-mini")
ANTHROPIC_MODEL = os.getenv("CDD_ANTHROPIC_MODEL", "claude-sonnet-4-20250514")

# %% [markdown]
# ## Diagram format support
#
# CDD supports three formats: Graphviz DOT, Mermaid, and PlantUML.

# %%
SUPPORTED_FORMATS = ["graphviz", "mermaid", "plantuml"]
DEFAULT_FORMAT = "graphviz"

# Public PlantUML render server. PlantUML is too heavyweight to bundle,
# so we use the public render endpoint. Documented in the report as a
# deliberate trade-off.
PLANTUML_SERVER = "https://www.plantuml.com/plantuml"

GRAPHVIZ_FORMAT = "png"
GRAPHVIZ_ENGINE = "dot"

DIAGRAM_TYPES = [
    "flowchart",
    "sequence",
    "class_diagram",
    "entity_relationship",
    "state_machine",
    "network_topology",
    "mind_map",
    "org_chart",
]

# %% [markdown]
# ## System prompts (per format)
#
# Each format gets its own prompt because the syntax is different.
# All prompts share the same rules: output only valid code, wrap in
# fenced code blocks, return the FULL diagram on modifications.

# %%
SYSTEM_PROMPTS = {
    "graphviz": """You are a diagramming assistant. Given a user's natural language
description, generate valid Graphviz DOT code.

Rules:
1. Output ONLY valid DOT code, wrapped in ```dot ... ``` markers.
2. No explanations before or after the code.
3. Use descriptive node labels.
4. Choose appropriate shapes:
   - Flowcharts: box for process, diamond for decision, oval for start/end
   - Class diagrams: record shapes
   - ER diagrams: box for entities, diamond for relationships
   - State machines: circle/doublecircle for states
5. Use colors and styles to improve readability.
6. Include a graph label with the diagram title.

If the user asks to modify an existing diagram, return the FULL updated
diagram, never a patch.""",

    "mermaid": """You are a diagramming assistant. Given a user's natural language
description, generate valid Mermaid diagram code.

Rules:
1. Output ONLY valid Mermaid code, wrapped in ```mermaid ... ``` markers.
2. No explanations before or after the code.
3. Start with the diagram type declaration (graph TD, sequenceDiagram, classDiagram, stateDiagram-v2, erDiagram, etc.).
4. Pick the diagram type that fits the request:
   - Flowcharts: graph TD or graph LR
   - Sequence: sequenceDiagram
   - Class: classDiagram
   - State: stateDiagram-v2
   - ER: erDiagram
5. Use clear node IDs and human-readable labels.
6. Use styling (classDef, style) where it improves clarity.

If the user asks to modify an existing diagram, return the FULL updated
diagram, never a patch.""",

    "plantuml": """You are a diagramming assistant. Given a user's natural language
description, generate valid PlantUML code.

Rules:
1. Output ONLY valid PlantUML code, wrapped in ```plantuml ... ``` markers.
2. No explanations before or after the code.
3. Always wrap in @startuml ... @enduml.
4. Pick the diagram type that fits the request:
   - Sequence diagrams: actor/participant + ->
   - Class diagrams: class with attributes/methods
   - State diagrams: [*] --> State
   - Component / deployment diagrams when appropriate
5. Use skinparam or styling directives where they improve readability.

If the user asks to modify an existing diagram, return the FULL updated
diagram, never a patch.""",
}

# %% [markdown]
# ## Vision-feedback loop
#
# The novel piece of the project. After rendering a diagram, send the
# image to a multimodal LLM with the user's intent and ask for a critique.
# If the critique flags issues, regenerate the diagram with the critique
# appended. Hard cap on iterations to prevent infinite loops.

# %%
VISION_FEEDBACK_ENABLED = True
VISION_MAX_ITERATIONS = 3

VISION_CRITIQUE_PROMPT = """You are reviewing a rendered diagram against a user's intent.

User's original intent:
{intent}

The diagram source code:
```
{code}
```

You will see the rendered diagram as an image (PNG).

Evaluate whether the diagram correctly expresses the user's intent and is
visually well-formed. Look for:
- Missing nodes, edges, or relationships from the intent
- Overlapping nodes or unreadable layout
- Wrong direction of arrows (e.g., for sequence/dependency)
- Wrong diagram type for what was asked
- Truncated or unreadable labels

Respond as JSON in this EXACT schema (no markdown, no prose):
{{
  "is_acceptable": true | false,
  "issues": ["short description of issue 1", "short description of issue 2"],
  "suggested_changes": "Concrete, actionable guidance for fixing the diagram. Empty string if is_acceptable is true."
}}"""

# %% [markdown]
# ## Description & suggestion prompt
#
# After the diagram is finalised, we ask a multimodal LLM to (a) describe what
# the diagram shows, in plain English, and (b) suggest concrete improvements
# or additions the user might consider. This is shown in the chat alongside
# the rendered image so the user gets both confirmation of what was built and
# ideas for the next refinement turn.

# %%
DESCRIBE_SUGGEST_PROMPT = """You are a diagram analyst. Look at the rendered
diagram and read its source code, then produce a short description and a
short list of suggestions.

Length rules — keep things tight:
- Description: 1-2 sentences. About 30-40 words total.
- Suggestions: 3 short bullets. Each one a single short sentence.
- Each suggestion should mention a specific element from the diagram by
  name, and propose a concrete change. Avoid vague advice.

User's original request:
{intent}

The diagram source code ({format}):
```
{code}
```

Respond as JSON in this EXACT schema (no markdown fences, no prose outside
the JSON):
{{
  "description": "Short description, 1-2 sentences.",
  "suggestions": [
    "Short suggestion mentioning a specific element.",
    "Short suggestion mentioning a specific element.",
    "Short suggestion mentioning a specific element."
  ]
}}"""

# %% [markdown]
# ## Evaluation rubric

# %%
EVAL_RUBRIC = {
    "syntax_valid": "Does the generated code parse without errors?",
    "node_accuracy": "Are all requested entities present as nodes?",
    "edge_accuracy": "Are relationships/connections correctly represented?",
    "layout_quality": "Is the diagram layout clean and readable?",
    "style_appropriate": "Are shapes, colors, and styles appropriate for the diagram type?",
    "vision_iterations": "How many vision-feedback iterations were needed (0 if disabled)?",
}