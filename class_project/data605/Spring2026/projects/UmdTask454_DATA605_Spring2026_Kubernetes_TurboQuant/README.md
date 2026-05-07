# Kubernetes TurboQuant — Multimodal Art Search

Deploy a CLIP-based image search engine on Kubernetes, with **TurboQuant**
compression to shrink the in-memory vector index ~8x while preserving search
quality.

## Architecture
```
[Notebook] -> [Ingestion svc] (CLIP embeddings via ONNX)
            -> [Search svc]    (text query -> ADC search)
            -> [Prometheus + Grafana]
```

Each service is a containerized FastAPI app deployed on Kubernetes. The
TurboQuant compression logic is a shared library imported by services that
need it.

## Layout
- `services/ingestion/` — FastAPI service, embeds images via ONNX CLIP
- `services/compression/` — TurboQuant library (shared)
- `benchmark.py` — local benchmark vs FAISS (SQ8, PQ)
- `template/` — class Docker template scripts (unused)

## Build the ingestion service

From this project directory:
```bash
cd services/ingestion
docker build -t tq-ingestion .
```

The build is multi-stage: the builder pulls `open_clip` + `torch` to export
CLIP's visual encoder to ONNX (~150 MB), then the runtime image only needs
`onnxruntime` + `fastapi`. Final image is ~600 MB.

## Run it locally
```bash
docker run --rm -p 8000:8000 tq-ingestion
```

In another terminal, send an image.

**Linux / macOS:**
```bash
curl -F "file=@path/to/image.jpg" http://localhost:8000/embed
```

**Windows (PowerShell):**
```powershell
curl.exe -F "file=@path\to\image.jpg" http://localhost:8000/embed
```

The response is a 512-dim normalized CLIP embedding.

## Endpoints
- `POST /embed` — multipart upload, returns `{"embedding": [...]}`
- `GET /healthz` — liveness probe
- `GET /metrics` — Prometheus metrics
