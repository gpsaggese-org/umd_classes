# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.16.0
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %% [markdown]
# # CDD API - Conversational Diagram Designer
#
# This notebook demonstrates the CDD system end-to-end. It is the canonical
# API tutorial that follows GP's `template.API.ipynb` pattern.
#
# **Pipeline:** natural language → LLM → diagram code → renderer → image
# → (optional) multimodal vision critique → corrected code → re-render → loop
# (cap: 3 iterations).
#
# **Supports:** Graphviz DOT, Mermaid, PlantUML.
#
# **How to run:**
# 1. `./docker_build.sh`
# 2. `./docker_jupyter.sh`
# 3. Open this notebook and run all cells
#
# Or launch the React UI: `./docker_app.sh` → http://localhost:8000

# %% [markdown]
# ## 1. Setup

# %%
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath("__file__")))

import cdd_config as config
import cdd_llm as llm
import cdd_renderer as renderer
from cdd_orchestrator import CDDOrchestrator
from IPython.display import Image, SVG, display

print(f"Default LLM provider: {config.LLM_PROVIDER}")
print(f"Supported formats: {config.SUPPORTED_FORMATS}")
print(f"Vision feedback enabled by default: {config.VISION_FEEDBACK_ENABLED}")
print(f"Vision iteration cap: {config.VISION_MAX_ITERATIONS}")

# %% [markdown]
# ## 2. Single-shot generation: Graphviz
#
# Generate a Graphviz DOT diagram from a natural language description.
# This is the simplest CDD interaction.

# %%
orch = CDDOrchestrator(format="graphviz")
prompt_1 = (
    "Draw a flowchart for user login: start, enter credentials, validate, "
    "if valid go to dashboard, if invalid show error and retry, "
    "max 3 retries then lock account"
)
diagram_source, image_bytes = orch.process_message(prompt_1)
print("Generated DOT source:")
print(diagram_source)

# %%
display(Image(data=image_bytes))
print(f"Iterations used: {len(orch.state.last_trace)}")

# %% [markdown]
# ## 3. Multi-turn refinement
#
# CDD keeps conversation history and modifies the existing diagram in place.

# %%
_, img2 = orch.process_message(
    "Add a 'Forgot Password' branch from login to email verification, "
    "then password reset, then back to login"
)
print(f"Revision: {orch.state.revision_count}")
display(Image(data=img2))

# %%
_, img3 = orch.process_message(
    "Add two-factor authentication after credential validation, before dashboard"
)
print(f"Revision: {orch.state.revision_count}")
display(Image(data=img3))

# %% [markdown]
# ## 4. Mermaid format
#
# Switching format means a new orchestrator (or reset). Here we generate a
# Mermaid sequence diagram. Mermaid renders via the public Kroki server, so
# this requires network access from the container.

# %%
orch_m = CDDOrchestrator(format="mermaid")
mermaid_prompt = (
    "Create a sequence diagram: A user clicks login. The browser sends "
    "credentials to the server. The server validates against the database "
    "and returns a session token. The browser stores it and redirects."
)
src_m, img_m = orch_m.process_message(mermaid_prompt)
print("Generated Mermaid source:")
print(src_m)
display(Image(data=img_m))

# %% [markdown]
# ## 5. PlantUML format
#
# PlantUML is rendered via the public PlantUML server (also network-dependent).

# %%
orch_p = CDDOrchestrator(format="plantuml")
plantuml_prompt = (
    "Class diagram: Animal (name, age), Dog extends Animal (breed), "
    "Cat extends Animal (indoor). Kennel has many Dogs."
)
src_p, img_p = orch_p.process_message(plantuml_prompt)
print("Generated PlantUML source:")
print(src_p)
display(Image(data=img_p))

# %% [markdown]
# ## 6. Vision feedback loop in action
#
# This is the centerpiece feature. With vision feedback enabled (the default),
# CDD renders the diagram, sends the image to a multimodal model, gets a
# critique, and iterates if the critique flags issues. Capped at 3 iterations.
#
# The trace recorded in `orch.state.last_trace` shows every step.

# %%
orch_v = CDDOrchestrator(format="graphviz", vision_feedback=True)
_, _ = orch_v.process_message(
    "Microservices architecture: API Gateway routes to three services "
    "(catalog, orders, payments). All three services share a Redis cache "
    "and a PostgreSQL database. Show clear hierarchy."
)
print("Trace from this turn (each entry is one pipeline step):")
for step in orch_v.state.last_trace:
    print(f"  {step}")

# %% [markdown]
# ## 7. Vision feedback OFF (single-shot baseline)
#
# For comparison: the same prompt with vision feedback disabled. This is
# the baseline we use in the evaluation study (`cdd.example.ipynb`).

# %%
orch_baseline = CDDOrchestrator(format="graphviz", vision_feedback=False)
_, _ = orch_baseline.process_message(
    "Microservices architecture: API Gateway routes to three services "
    "(catalog, orders, payments). All three services share a Redis cache "
    "and a PostgreSQL database. Show clear hierarchy."
)
print("Trace (vision off — should show only one iteration):")
for step in orch_baseline.state.last_trace:
    print(f"  {step}")

# %% [markdown]
# ## 8. Different diagram types

# %%
orch_class = CDDOrchestrator(format="graphviz")
_, img_c = orch_class.process_message(
    "Create a class diagram: Book (title, isbn, price), Author (name, bio), "
    "Customer (name, email), Order (date, total). Author writes many Books. "
    "Customer places many Orders. Order contains many Books."
)
display(Image(data=img_c))

# %%
orch_sm = CDDOrchestrator(format="graphviz")
_, img_s = orch_sm.process_message(
    "State machine for an order: Draft -> Submitted -> Under Review -> "
    "Approved or Rejected. Approved -> Fulfilled -> Closed. Rejected -> Draft."
)
display(Image(data=img_s))

# %% [markdown]
# ## 9. Export

# %%
orch.export_dot("/tmp/login_flow.dot")
orch.export_image("/tmp/login_flow.png", fmt="png")
orch.export_image("/tmp/login_flow.svg", fmt="svg")
print("Exported DOT, PNG, SVG to /tmp/")

# %% [markdown]
# ## 10. Validation
#
# The renderer validates source before rendering, so syntax errors are
# caught early and surface a clear error.

# %%
bad_dot = "digraph { this is invalid }"
is_valid, error = renderer.validate(bad_dot, "graphviz")
print(f"Bad DOT — Valid: {is_valid}, Error: {error[:80]}")

good_dot = 'digraph { A -> B -> C; A [label="Start"]; C [label="End"]; }'
is_valid, _ = renderer.validate(good_dot, "graphviz")
print(f"Good DOT — Valid: {is_valid}")
display(Image(data=renderer.render(good_dot, "graphviz")))

# %% [markdown]
# ## 11. State inspection

# %%
import json

state = orch.get_state_dict()
print(f"Format: {state['format']}")
print(f"Revisions: {state['revision_count']}")
print(f"Conversation turns: {len(state['conversation_history']) // 2}")
print(f"Last trace step count: {len(state['last_trace'])}")
