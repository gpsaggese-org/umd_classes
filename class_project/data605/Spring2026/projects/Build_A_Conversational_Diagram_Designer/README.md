# Conversational Diagram Designer (CDD)

DATA 605 - Big Data Systems | Spring 2026 | Prof. GP Saggese

CDD is a browser-based diagramming tool that turns natural-language descriptions into rendered technical diagrams. The user types a request, an LLM generates valid diagram source code in one of three formats, the system renders it to an image, and a multimodal vision-feedback loop inspects the rendered output and self-corrects up to three times. The full stack runs from a single Docker image and supports both a notebook-driven workflow (Jupyter) and a web application (FastAPI + React).

The project is framed as a multi-stage inference pipeline with vision-in-the-loop validation, response caching, and an empirical evaluation comparing diagram quality with the loop on versus off.

## What the system does

1. The user describes a diagram in plain English ("class diagram for an e-commerce app", "state machine for an order lifecycle").
2. CDD selects a format (Graphviz DOT, Mermaid, or PlantUML) and asks the LLM to produce valid source code.
3. The renderer converts source code to a PNG image and an SVG.
4. With vision feedback enabled, the rendered image and the original user intent go back to the multimodal model. The model returns a structured critique: is the diagram acceptable, what is wrong, what should change.
5. If the critique flags issues and the iteration counter is below the cap, the orchestrator regenerates the diagram with the critique appended to the prompt.
6. The user sees the final diagram, the source code, and the iteration trace. They can refine through follow-up messages, export to PNG, SVG, or source, or switch formats mid-conversation.

The design honors three explicit goals from the project brief: browser-based delivery, real-time rendering, and vision-driven self-correction. It also stays inside the brief's stated non-goals: no multi-user collaboration, no authentication, no diagram persistence beyond the active session.

## Supported formats

| Format | Renderer | Local | Notes |
|---|---|---|---|
| Graphviz DOT | `graphviz` Python binding (system `dot`) | Yes | Used for flowcharts, class diagrams, ER diagrams, state machines, mind maps. |
| Mermaid | Kroki public render server | No | Used for sequence diagrams, modern flowcharts, journey maps. |
| PlantUML | Public PlantUML render server | No | Used for UML sequence, class, state, and component diagrams. |

The Mermaid and PlantUML choices are documented as deliberate trade-offs. Both formats have browser-only library options, but the CheerpJ-based PlantUML library has known correctness issues on complex diagrams, and Mermaid's bundle size adds non-trivial weight to the frontend. Server-rendering through Kroki and the official PlantUML server produces consistent output and keeps the frontend lean.

## Architecture

The diagram below shows the full request lifecycle — from user message through LLM code generation, rendering, and the optional vision-feedback loop, down to the evaluation harness that benchmarks the pipeline in both vision-on and vision-off modes.


<img width="1175" height="1600" alt="image" src="https://github.com/user-attachments/assets/0ce06fca-0a72-42bf-8d96-49cbfa0220a3" />



Pipeline walkthrough
user message
  -> cdd_llm.generate(prompt, format)            text -> diagram code
  -> cdd_renderer.render(code, format)           code -> PNG / SVG
  -> if vision feedback enabled:
       -> cdd_llm.critique_image(png, intent)    PNG + intent -> JSON critique
       -> if not acceptable and iter < 3:
            regenerate with critique appended
            loop
  -> return final code, image, and trace
  

The entire pipeline lives behind a single `CDDOrchestrator` class. The frontend talks to the orchestrator through a small FastAPI surface (`/api/chat`, `/api/export`, `/api/reset`, `/api/config`). The orchestrator records every step of the pipeline so the report can show what happened during a turn: which mode ran, how many iterations the vision loop used, what each iteration produced.

## Layout

```
cdd_config.py           Provider settings, format definitions, system prompts, vision config
cdd_llm.py              Unified text and multimodal client. Gemini primary; OpenAI / Anthropic optional fallbacks
cdd_renderer.py         Three-format render(code, format). Validation and image conversion
cdd_orchestrator.py     The user-turn state machine and the vision-feedback loop
cdd_eval.py             Benchmark harness. Vision-on vs vision-off comparison
cdd_server.py           FastAPI backend. Serves the React app and the API

cdd.API.ipynb           API tutorial notebook (paired with cdd.API.py via jupytext)
cdd.example.ipynb       Evaluation study notebook (paired with cdd.example.py via jupytext)

frontend/               React + Vite single-page chat UI
test/                   Pytest suite (46 passing, 2 network-only skipped)

Dockerfile              Single image: Python 3.11 + Jupyter + FastAPI + built React
docker_build.sh         Build the image
docker_jupyter.sh       Run with Jupyter on :8888 (the notebook-driven workflow)
docker_app.sh           Run as a web app on :8000 (FastAPI + React UI)
docker_bash.sh          Open an interactive shell inside the container

requirements.txt        Python dependencies
.env.example            Environment variable template (copy to .env)
CONTRIBUTORS.md         File-ownership map
README.md               This file
```

## Quickstart

### 1. Get a Gemini API key

The default LLM provider is Gemini 2.5 Flash. Get a free-tier key at [aistudio.google.com/apikey](https://aistudio.google.com/apikey).

### 2. Configure environment

```bash
cp .env.example .env
# Open .env and paste your GEMINI_API_KEY
```

OpenAI and Anthropic keys can also be added; the system will surface whichever providers are configured.

### 3. Build the Docker image

```bash
./docker_build.sh
```

### 4. Run

Two run modes share the same image. Pick whichever fits the task.

**Notebook workflow.** Start Jupyter and open the tutorial notebooks. This is the workflow used for grading.

```bash
./docker_jupyter.sh
```
Open [http://localhost:8888](http://localhost:8888) and run `cdd.API.ipynb` for the API tour, or `cdd.example.ipynb` for the evaluation study.

**Web app.** Start the FastAPI server and open the React UI.

```bash
./docker_app.sh
```
Open [http://localhost:8000](http://localhost:8000). Type a description, switch formats from the dropdown, toggle the vision feedback loop, refine through follow-up messages, and export to PNG / SVG / source.

### 5. Run the test suite

```bash
./docker_bash.sh
# Inside the container:
pytest test/test_docker_all.py -v
```

Expected result: 46 tests pass, 2 skipped. The skipped tests are integration tests against Kroki (Mermaid) and the public PlantUML server; they are skipped by default to keep the suite hermetic.

## Vision-feedback loop

The vision loop is the project's central novel feature. Most chat-to-diagram systems generate code blind: the LLM never sees what its own output looks like. CDD closes that loop by sending the rendered diagram back to a multimodal model along with the original intent and a structured critique prompt. The model returns a JSON critique with three fields: `is_acceptable`, a list of `issues`, and a `suggested_changes` string. If the critique flags issues and the iteration counter is below three, the orchestrator builds a correction prompt that includes the critique and regenerates.

The loop is bounded. Three iterations is the hard cap, matching the recommendation in the project brief. Each iteration is logged in the turn trace so the report can show how often the loop converges, when it makes a diagram better, and the rare cases where it makes a diagram worse.

## Evaluation

`cdd_eval.py` runs a curated benchmark of prompts across all three formats and three complexity tiers. Each prompt is generated twice: once with the vision feedback loop disabled (a single-shot baseline) and once with it enabled (up to three iterations). Per-output metrics include syntax validity, render success, node count, edge count, label presence, and styling presence. An optional LLM-as-judge step rates semantic correctness and visual quality on a 1-5 scale using a versioned rubric prompt.

The full evaluation, summary tables, and side-by-side renderings live in `cdd.example.ipynb`. Results are written to a JSON file for downstream analysis and the project report.

## Configuration

All knobs live in `cdd_config.py` and `.env`.

| Variable | Default | Effect |
|---|---|---|
| `CDD_LLM_PROVIDER` | `gemini` | One of `gemini`, `openai`, `anthropic` |
| `GEMINI_API_KEY` | (required for default) | Free-tier key from Google AI Studio |
| `CDD_GEMINI_MODEL` | `gemini-2.5-flash` | Multimodal model used for both generation and critique |
| `OPENAI_API_KEY` | (optional) | Enables OpenAI as a fallback provider |
| `ANTHROPIC_API_KEY` | (optional) | Enables Anthropic as a fallback provider |
| `VISION_FEEDBACK_ENABLED` | `True` | Master switch for the vision loop |
| `VISION_MAX_ITERATIONS` | `3` | Hard cap on loop iterations per turn |

## Engineering notes

- The system has one Docker image. Both run modes (Jupyter and web app) use the same image with different entrypoints. This keeps the build cache hot, the dependency graph in sync, and the grading flow simple.
- Frontend is a single-file React component (no build pipeline beyond Vite, no UI framework, no state library). The render code paths and the orchestrator state machine are exercised the same way in tests as they are in the UI.
- The renderer accepts any of the three formats through one entry point, which keeps the orchestrator format-agnostic and lets the eval harness sweep across formats with a single loop.
- Jupytext-paired `.py` and `.ipynb` files mean the notebooks can be diffed and code-reviewed as plain Python, while staying executable as full notebooks. This matches the project template convention.

## What is explicitly out of scope

The project brief lists multi-user collaboration, authentication, and diagram persistence as non-goals for V1, and the design respects all three. No login system, no shared sessions, no database. The cache that exists is for LLM responses only, not user content. AWS deployment is a possible follow-up but is not part of the current deliverable.
