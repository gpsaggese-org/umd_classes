import json
import time
from pathlib import Path

import faiss
import numpy as np
import open_clip
import torch

from services.compression.turboquant_adc import TurboQuantIndex

ROOT = Path(__file__).parent
DATA_DIR = ROOT / "data"

QUERIES = [
    "a dark knight in heavy armor",
    "beautiful sunset over the ocean",
    "cute animal portrait",
    "futuristic city skyline at night",
    "portrait of a woman with flowers",
    "abstract geometric art",
    "dragon breathing fire",
    "cozy cabin in the snow",
    "underwater scene with fish",
    "vintage car on a desert road",
    "samurai warrior in battle",
    "magical forest with glowing mushrooms",
    "astronaut floating in space",
    "oil painting of a castle",
    "steampunk mechanical bird",
    "neon cyberpunk street scene",
    "peaceful zen garden",
    "wolf howling at the moon",
    "art deco poster design",
    "stormy seascape with lighthouse",
]


def main():
    embeddings = np.load(DATA_DIR / "embeddings.npy")
    N, D = embeddings.shape
    print(f"Dataset: {N} vectors, dim={D}\n")

    index_fp32 = faiss.IndexFlatIP(D)
    index_fp32.add(embeddings)

    db = torch.from_numpy(embeddings)
    tq3 = TurboQuantIndex(dim=D, bits=3)
    tq3.add(db)
    tq4 = TurboQuantIndex(dim=D, bits=4)
    tq4.add(db)

    index_sq8 = faiss.IndexScalarQuantizer(D, faiss.ScalarQuantizer.QT_8bit, faiss.METRIC_INNER_PRODUCT)
    index_sq8.train(embeddings)
    index_sq8.add(embeddings)

    index_pq = faiss.IndexPQ(D, 64, 8, faiss.METRIC_INNER_PRODUCT)
    index_pq.train(embeddings)
    index_pq.add(embeddings)

    model, _, _ = open_clip.create_model_and_transforms(
        "ViT-B-32", pretrained="laion2b_s34b_b79k"
    )
    tokenizer = open_clip.get_tokenizer("ViT-B-32")
    model = model.eval()

    qs = []
    for q in QUERIES:
        tokens = tokenizer([q])
        with torch.no_grad():
            e = model.encode_text(tokens)
            e = e / e.norm(dim=-1, keepdim=True)
        qs.append(e.float())
    qb = torch.cat(qs, dim=0)
    qnp = qb.numpy()

    k = 10
    _, gt = index_fp32.search(qnp, k)

    def recall(ids):
        rs = []
        for i in range(len(QUERIES)):
            gs = set(gt[i].tolist())
            rs_ = ids[i].tolist() if isinstance(ids[i], np.ndarray) else ids[i].numpy().tolist()
            rs.append(len(gs & set(rs_)) / k)
        return np.mean(rs)

    fp32_mb = N * D * 4 / (1024 ** 2)

    print(f"{'Method':<25} {'Recall@10':>10} {'Memory':>12} {'Ratio':>8}")
    print("-" * 60)
    print(f"{'FP32 exact':<25} {'1.000':>10} {fp32_mb:>9.1f} MB {'1.0x':>8}")

    _, ids = index_sq8.search(qnp, k)
    print(f"{'FAISS SQ8':<25} {recall(ids):>10.3f} {N*D/1024**2:>9.1f} MB {'4.0x':>8}")

    _, ids = index_pq.search(qnp, k)
    print(f"{'FAISS PQ (64x8)':<25} {recall(ids):>10.3f} {N*64/1024**2:>9.1f} MB {D*4/64:>7.1f}x")

    for bits, tq in [(3, tq3), (4, tq4)]:
        _, ids = tq.search(qb, k=k)
        mem = tq.memory_bytes()
        print(f"{'TQ ' + str(bits) + '-bit ADC':<25} {recall(ids):>10.3f} {mem['compressed_mb']:>9.2f} MB {mem['compression_ratio']:>7.1f}x")

    print("\n--- With FP32 rerank (top-k*2 → rescore → top-k) ---")
    for bits, tq in [(3, tq3), (4, tq4)]:
        _, ids = tq.search(qb, k=k, rerank=True, rerank_mult=2, fp32_vectors=embeddings)
        mem = tq.memory_bytes()
        print(f"{'TQ ' + str(bits) + '-bit + rerank':<25} {recall(ids):>10.3f} {mem['compressed_mb']:>9.2f} MB {mem['compression_ratio']:>7.1f}x")


if __name__ == "__main__":
    main()
