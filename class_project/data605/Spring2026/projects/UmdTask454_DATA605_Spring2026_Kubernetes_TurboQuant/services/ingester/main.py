import json
import os
import tarfile
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import numpy as np
import requests

SHARD = int(os.environ["JOB_COMPLETION_INDEX"])
N_SHARDS = int(os.environ["N_SHARDS"])
DATASET_URL = os.environ["DATASET_URL"]
EMBEDDER_URL = os.environ["EMBEDDER_URL"]
OUTPUT_DIR = Path(os.environ["OUTPUT_DIR"])
BATCH_SIZE = int(os.environ["BATCH_SIZE"])
CONCURRENCY = int(os.environ["CONCURRENCY"])
LIMIT = int(os.environ["LIMIT"])
LOCAL_IMAGES = Path("/tmp/images")


def fetch_dataset():
    archive = "/tmp/images.tar"
    print(f"shard {SHARD}: downloading {DATASET_URL}", flush=True)
    t0 = time.time()
    urllib.request.urlretrieve(DATASET_URL, archive)
    print(f"shard {SHARD}: extracting (download took {time.time() - t0:.1f}s)", flush=True)
    LOCAL_IMAGES.mkdir(parents=True, exist_ok=True)
    with tarfile.open(archive, "r") as tf:
        tf.extractall(LOCAL_IMAGES)
    os.remove(archive)


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    fetch_dataset()

    files = sorted(LOCAL_IMAGES.glob("*.jpg"))
    if LIMIT > 0:
        files = files[:LIMIT]
    my_files = [f for i, f in enumerate(files) if i % N_SHARDS == SHARD]
    print(f"shard {SHARD}/{N_SHARDS}: {len(my_files)} of {len(files)} files", flush=True)

    def process_batch(batch):
        files_field = [("files", (f.name, f.read_bytes(), "image/jpeg")) for f in batch]
        r = requests.post(EMBEDDER_URL, files=files_field, timeout=300)
        r.raise_for_status()
        return r.json()["embeddings"], [f.name for f in batch]

    batches = [my_files[i : i + BATCH_SIZE] for i in range(0, len(my_files), BATCH_SIZE)]
    embeddings = []
    filenames = []
    t0 = time.time()
    with ThreadPoolExecutor(max_workers=CONCURRENCY) as pool:
        futures = [pool.submit(process_batch, b) for b in batches]
        for batch_n, fut in enumerate(as_completed(futures), 1):
            embs, names = fut.result()
            embeddings.extend(embs)
            filenames.extend(names)
            rate = len(filenames) / (time.time() - t0)
            print(f"shard {SHARD}: batch {batch_n}/{len(batches)} ({rate:.1f} img/s)", flush=True)

    arr = np.array(embeddings, dtype=np.float32)
    np.save(OUTPUT_DIR / f"shard_{SHARD:03d}.npy", arr)
    with open(OUTPUT_DIR / f"shard_{SHARD:03d}.json", "w") as f:
        json.dump(filenames, f)
    print(f"shard {SHARD}: done, wrote {arr.shape}", flush=True)


if __name__ == "__main__":
    main()
