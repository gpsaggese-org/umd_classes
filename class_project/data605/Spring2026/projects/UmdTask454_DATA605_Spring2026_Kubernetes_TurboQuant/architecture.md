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

### Worked example

A toy version of what the code at `services/compression/turboquant_adc.py` is doing. Sized down to `d = 4` with a 1-bit MSE codebook so the arithmetic fits on screen.

**Setup:**

- Codebook (the 2 MSE centroids in the rotated space): `c = [c₀, c₁] = [−0.5, +0.5]`
- DB vector — stored as the *compressed* tuple:
  - `indices = [1, 0, 1, 1]` (one index per coord, 4 bits total)
  - `norm = 2.0` (one fp32 scalar)
  - *(QJL residual sign bits omitted here — same trick, second term)*
- Query stays fp32: `q = [+0.3, +0.2, +0.4, −0.1]`

The vector those bits *would* reconstruct to is `x̂ = norm · [c[i] for i in indices] = 2.0 · [+0.5, −0.5, +0.5, +0.5] = [+1, −1, +1, +1]`. **We never actually build this.**

**Naive path (the one we're avoiding):** decompress, then dot.

```
⟨q, x̂⟩ = 0.3·(+1) + 0.2·(−1) + 0.4·(+1) + (−0.1)·(+1) = 0.40
```

That requires materializing the full `d`-dim `x̂` for *every* DB vector. Across millions of vectors, that's the cost ADC skips.

**ADC path:**

*Step 1 — build the lookup table once per query.* This is the only time `q` "meets" the codebook:

```
LUT[k, d] = q[d] · c[k]            shape: (#centroids, d) = (2, 4)

LUT[0, :] = q · (−0.5) = [−0.15, −0.10, −0.20, +0.05]
LUT[1, :] = q · (+0.5) = [+0.15, +0.10, +0.20, −0.05]
```

`2·d = 8` multiplies, paid *once* for the whole query batch.

*Step 2 — score each DB vector with `d` lookups + `d` adds + one multiply:*

```
For x with indices [1, 0, 1, 1]:

  partial = LUT[1, 0] + LUT[0, 1] + LUT[1, 2] + LUT[1, 3]
          =  +0.15    +  (−0.10)  +  +0.20    +  (−0.05)
          =  +0.20

  ⟨q, x̂⟩  ≈  norm · partial  =  2.0 · 0.20  =  0.40   ✓
```

Same answer — and `x̂` was never reconstructed in memory. The compressed bits act as **pointers into a per-query lookup table**, not as something we decompress.

**Why this works:** the inner product is linear in the database vector. So we precompute, once per query, the contribution each codebook entry *would* make to the dot product. After that, scoring a DB vector is just: read its `d` indices, sum that many entries from the LUT, multiply by the stored norm.

**Cost comparison per DB vector:**

| Path | Work |
|---|---|
| Decompress + dot | `d` muls to reconstruct + `d` muls + `d−1` adds for dot = **2d MUL + (d−1) ADD** + materialize a `d`-vector |
| ADC | `d` LUT reads + `d−1` adds + 1 mul by norm = **1 MUL + (d−1) ADD** |

The LUT-build cost (`2·d` per query) amortizes across all `N` DB vectors, so for large `N` the per-vector cost is what dominates.
