# Conversational Diagram Designer (CDD)

DATA 605 - Big Data Systems | Spring 2026 | Prof. GP Saggese

A browser-based diagramming tool where users create and refine diagrams
using natural language. CDD generates diagram code in three formats
(Graphviz DOT, Mermaid, PlantUML), renders the code to an image, and
uses a multimodal vision-feedback loop (3-iteration cap) to validate
and self-correct the rendered output.

## What's in this project

```
.
├── cdd_config.py         # LLM provider, formats, system prompts, vision config
├── cdd_llm.py            # Gemini / OpenAI / Anthropic clients (text + multimodal)
├── cdd_renderer.py       # Unified render(code, format) for Graphviz/Mermaid/PlantUML
├── cdd_orchestrator.py   # Pipeline: generate -> render -> critique -> iterate
├── cdd_eval.py           # Evaluation harness (vision-on vs vision-off study)
├── cdd_server.py         # FastAPI backend serving the React UI
│
├── cdd.API.ipynb         # API tutorial notebook (paired with cdd.API.py)
├── cdd.example.ipynb     # Evaluation study notebook (paired with cdd.example.py)
│
├── frontend/             # React + Vite chat UI
├── test/                 # pytest suite (46 passing)
│
├── Dockerfile            # Single image: Python + Jupyter + FastAPI + built React
├── docker_build.sh       # ./docker_build.sh
├── docker_jupyter.sh     # Jupyter at :8888 (notebook-driven workflow)
├── docker_app.sh         # FastAPI + React UI at :8000
├── docker_bash.sh        # Interactive shell in the container
│
├── requirements.txt
├── .env.example          # Copy to .env, add Gemini API key
└── README.md
```

## Quickstart

### 1. Get a Gemini API key (free tier)

Visit [aistudio.google.com/apikey](https://aistudio.google.com/apikey).

### 2. Set up `.env`

```bash
cp .env.example .env
# Edit .env and paste your GEMINI_API_KEY
```

### 3. Build the Docker image

```bash
./docker_build.sh
```

### 4. Run it

Two ways, depending on what you want to do:

**Option A: Jupyter (GP's grading flow)**
```bash
./docker_jupyter.sh
```
Open [http://localhost:8888](http://localhost:8888), then run `cdd.API.ipynb`
or `cdd.example.ipynb`.

**Option B: Web app**
```bash
./docker_app.sh
```
Open [http://localhost:8000](http://localhost:8000).

### 5. Run tests

```bash
./docker_bash.sh
# Inside the container:
pytest test/test_docker_all.py -v
```

You should see 46 tests pass and 2 skipped (the skipped tests require network
to Mermaid/PlantUML rendering servers).

## Architecture

The pipeline for one user turn:

```
user message
  -> cdd_llm.generate(prompt, format)        # text -> diagram code
  -> cdd_renderer.render(code, format)        # code -> PNG bytes
  -> if vision feedback enabled:
       -> cdd_llm.critique_image(png, intent) # PNG + text -> JSON critique
       -> if not acceptable and iterations < 3:
            -> regenerate with critique appended
            -> loop
  -> return final code, image, and trace
```

`cdd_orchestrator.py` glues these together. `cdd_eval.py` runs the same
pipeline against benchmark prompts in both vision-on and vision-off
conditions and produces comparable metrics.

## Format support

| Format | Renderer | Network needed |
|---|---|---|
| Graphviz DOT | Local `graphviz` binary in container | No |
| Mermaid | Public Kroki render server | Yes |
| PlantUML | Public PlantUML render server | Yes |

The Mermaid and PlantUML choices are documented in the project report
under "Trade-offs." Both have browser-only library options that we
rejected for correctness reasons (the CheerpJ-based PlantUML library
has known rendering bugs on complex diagrams that would corrupt the
evaluation data).

## Vision-feedback loop

The loop renders the diagram, sends the image plus the user's intent
to a multimodal LLM, parses a JSON critique, and either accepts the
diagram or rebuilds it with the critique appended to the next prompt.
Hard cap at 3 iterations.

The loop's effectiveness is measured empirically in `cdd.example.ipynb`
by running each benchmark prompt twice (vision-off vs vision-on) and
comparing metrics. Results are saved to JSON for the report.

## Team

| Member | Role |
|---|---|
| Niveda Jawahar | Lead — backend (LLM client, server, infrastructure) |
| Member 2 | Frontend — React UI, renderer, three-format pipeline |
| Member 3 | Orchestrator, vision-feedback loop, evaluation study |

See `CONTRIBUTORS.md` for the file-ownership map.
