# Architecture

Three Docker images:

- **`tq-embedder`** — FastAPI service that takes a batch of JPEGs and returns CLIP embeddings. Deployed as a K8s Deployment + HPA (scales 1→5 on CPU).
- **`tq-ingester`** — One-shot K8s Job that downloads the dataset, POSTs batches to the embedder, and writes embedding shards to `/data/embeddings/`.
- **`tq-demo`** — JupyterLab container running the notebook: combines the shards, runs TurboQuant compression, computes recall, and visualizes results.

The host's `./data/` dir is shared with the cluster via `minikube mount` and with the demo container via a bind mount, so all three see the same files.

## TurboQuant compression

Two-stage scalar quantization:

1. **Rotate** each vector by a random orthogonal matrix. Coordinates then follow a known Beta distribution where scalar quantization is near-optimal.
2. **MSE stage** — quantize each rotated coordinate to `bits-1` bits using a precomputed codebook (centroids minimize MSE under the Beta distribution).
3. **QJL stage** — encode the residual at 1 bit per dim via a random-sign projection. Recovers precision the MSE stage lost.

Stored per vector: stage-1 indices, stage-2 signs, original norm, residual norm. At 3 bits/dim on 512-d embeddings, ~10× smaller than FP32.

## Asymmetric distance (ADC)

Queries stay FP32 (rotated the same way as the DB). So, how do we calculate distance between a DB compressed vector and a non compressed query vector?

1. for each rotated query coord, multiply by the centroid the DB stored. This will be a vector where each position (index) is the value of the centroid.
2. Add a correction term: project the query through the QJL sign matrix and dot with the stored signs.
3. Multiply by the stored norm.

"asymmetric" because the query is full-precision and the DB is compressed. we do not decompress the vectors to perform distance calc.
