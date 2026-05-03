# Contributors

This document maps the project's files to their owners. Used for
contribution attribution and referenced in the project report.

## Team

| Member | Role | Domain |
|---|---|---|
| Niveda Jawahar | Lead | Backend, LLM, infrastructure |
| Member 2 | Frontend / Renderer | React UI, three-format rendering |
| Member 3 | Orchestrator / Eval | Vision loop, evaluation study |

## File ownership

### Member 1 (Niveda — Lead)

Owns the backend pipeline core, LLM integration, server, and Docker infrastructure.

```
cdd_config.py         Configuration, system prompts, vision-loop parameters
cdd_llm.py            LLM client (Gemini text + multimodal, OpenAI/Anthropic fallbacks)
cdd_server.py         FastAPI backend serving the React UI
cdd.API.ipynb         API tutorial notebook (canonical CDD demo)
cdd.API.py            Jupytext-paired source for cdd.API.ipynb
Dockerfile            Single-container build (Python + Jupyter + FastAPI + React)
requirements.txt      Python dependencies
docker_build.sh       Build the Docker image
docker_jupyter.sh     Run Jupyter (notebook-driven workflow)
docker_app.sh         Run the FastAPI + React app
docker_bash.sh        Open an interactive shell in the container
.env.example          Environment variable template
.gitignore
README.md             Project overview and quickstart
CONTRIBUTORS.md       This file
```

### Member 2 (Frontend / Renderer)

Owns the rendering pipeline (three formats, unified API) and the entire
React UI including the API client.

```
cdd_renderer.py                  Unified renderer for Graphviz/Mermaid/PlantUML
frontend/package.json            Frontend dependencies
frontend/vite.config.js          Vite build config
frontend/index.html              HTML entry point
frontend/src/main.jsx            React entry
frontend/src/App.jsx             Three-pane chat UI (chat + code + preview)
frontend/src/api.js              Typed API client for the backend
```

### Member 3 (Orchestrator / Eval)

Owns the orchestration logic (including the vision-feedback loop), the
empirical evaluation harness, and the project's test suite.

```
cdd_orchestrator.py        State machine + 3-iteration vision loop + syntax repair
cdd_eval.py                Evaluation harness (vision-on vs vision-off comparison)
cdd.example.ipynb          Evaluation study notebook
cdd.example.py             Jupytext-paired source for cdd.example.ipynb
test/__init__.py
test/test_docker_all.py    48 tests across 9 sections (46 pass, 2 network-only skipped)
```

## Commit order

Because Member 2's renderer depends on Member 1's config, and Member 3's
orchestrator and eval depend on both Member 1 and Member 2, the team
commits in this order:

1. **Member 1 first.** Adds the LLM core, server, infrastructure.
2. **Member 2 second.** Adds the renderer and React UI.
3. **Member 3 last.** Adds the orchestrator, eval, and full test suite.

After all three commits land, the test suite runs cleanly and
`./docker_app.sh` brings up the working stack.

## Final report contribution table

The project report includes an explicit contribution table summarizing
deliverables per member with commit counts and PR counts. Generated
from `git log --author=` at the end of the project.
