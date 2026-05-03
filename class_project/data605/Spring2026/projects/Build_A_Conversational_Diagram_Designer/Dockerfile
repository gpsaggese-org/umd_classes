# ============================================================
# CDD Project Dockerfile
# Single container: Python + Jupyter + FastAPI + React (built)
# Two ways to run after build:
#   ./docker_jupyter.sh  -> Jupyter at :8888 (GP's grading flow)
#   ./docker_app.sh      -> FastAPI + React UI at :8000
# ============================================================

# --- Stage 1: Build React frontend ---
FROM node:20-slim AS frontend-build
WORKDIR /frontend

# Copy manifest first for layer caching. The wildcard tolerates an absent
# package-lock.json; npm will create one on first build.
COPY frontend/package.json frontend/package-lock.json* ./
RUN npm install

COPY frontend/ .
RUN npm run build

# --- Stage 2: Python runtime ---
FROM python:3.11-slim

WORKDIR /app

# System deps:
#   graphviz: needed by the cdd_renderer.py local Graphviz path
#   ca-certificates, curl: useful for diagnostics + outbound HTTPS to
#                          kroki.io (Mermaid) and plantuml.com
RUN apt-get update && apt-get install -y --no-install-recommends \
    graphviz \
    ca-certificates \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Project source
COPY . .

# Built React app from stage 1
COPY --from=frontend-build /frontend/dist /app/frontend/dist

# Expose ports: 8888 Jupyter, 8000 FastAPI
EXPOSE 8888 8000

# Default: Jupyter (GP's grading flow)
CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", \
     "--no-browser", "--allow-root", "--NotebookApp.token=''"]
