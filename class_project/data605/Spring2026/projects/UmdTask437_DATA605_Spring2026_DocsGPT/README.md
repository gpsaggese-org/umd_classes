# DocsGPT Tutorial — Intelligent Documentation Assistant

DocsGPT is an open-source, RAG-based AI platform (15k+ GitHub stars) that
retrieves relevant document chunks and passes them to a language model to
generate grounded answers. This tutorial builds a complete documentation
assistant on top of the DocsGPT Cloud API — covering summarisation, FAQ
generation, evaluation, multi-language output, streaming, and an interactive UI.

## Quick Start

```bash
cd tutorials/docsgpt
cp .env.example .env          # add your agent key to .env
./docker_build.sh             # build the Docker image
./docker_jupyter.sh           # launch Jupyter Lab at localhost:8888
```

Get your Agent key: https://app.docsgpt.cloud → Settings → Agents → Create New

Open **http://localhost:8888** and work through the notebooks in order:

1. **`docsgpt.API.ipynb`** (20 min) — Walks through every real DocsGPT Cloud
   endpoint with raw HTTP calls and `docsgpt_utils` wrapper calls side by side:
   `/api/answer`, `/stream`, `/api/store_attachment`, `/api/task_status`.
   Also covers multi-turn conversation, SSE streaming, and the file attachment flow.

2. **`docsgpt.example.ipynb`** (25 min) — End-to-end documentation assistant:
   loads data from three real datasets (Awesome ML, Stack Overflow, The Pile),
   summarises each document, generates FAQs, evaluates output with ROUGE + BLEU,
   produces multi-language output in 9 languages, and launches an interactive
   Gradio UI.


## Key files

| File | Purpose |
|------|---------|
| `docsgpt_utils.py` | All reusable functions and API wrappers |
| `docsgpt.API.ipynb` + `.py` | API walkthrough (Jupytext paired) |
| `docsgpt.example.ipynb` + `.py` | Full application (Jupytext paired) |
| `Dockerfile` + `docker_*.sh` | Container setup and management |
| `requirements.txt` | Pinned Python dependencies |
| `.env.example` | Template for API key configuration |

See [project template README](../../project_template_README.md) for full
Docker usage details.