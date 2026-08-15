import io
import os
from typing import List

import numpy as np
import onnxruntime as ort
from fastapi import FastAPI, File, HTTPException, UploadFile
from PIL import Image
from prometheus_fastapi_instrumentator import Instrumentator

CLIP_MEAN = np.array([0.48145466, 0.4578275, 0.40821073], dtype=np.float32)
CLIP_STD = np.array([0.26862954, 0.26130258, 0.27577711], dtype=np.float32)
MODEL_PATH = "/app/clip_visual.onnx"
ONNX_THREADS = int(os.environ["ONNX_THREADS"])

app = FastAPI(title="TurboQuant Embedder")
sess_options = ort.SessionOptions()
sess_options.intra_op_num_threads = ONNX_THREADS
sess_options.inter_op_num_threads = 1
session = ort.InferenceSession(MODEL_PATH, sess_options=sess_options, providers=["CPUExecutionProvider"])
Instrumentator().instrument(app).expose(app)


def preprocess(image):
    image = image.convert("RGB").resize((224, 224), Image.BICUBIC)
    arr = np.asarray(image, dtype=np.float32) / 255.0
    arr = (arr - CLIP_MEAN) / CLIP_STD
    return arr.transpose(2, 0, 1)


@app.get("/healthz")
def healthz():
    return {"status": "ok"}


@app.post("/embed")
def embed(files: List[UploadFile] = File(...)):
    tensors = []
    for f in files:
        try:
            img = Image.open(io.BytesIO(f.file.read()))
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"invalid image {f.filename}: {e}")
        tensors.append(preprocess(img))

    batch = np.stack(tensors, axis=0)
    feats = session.run(None, {"image": batch})[0]
    # normalize and avoid divide by 0 edge case
    feats /= np.linalg.norm(feats, axis=1, keepdims=True) + 1e-12
    return {"embeddings": feats.tolist()}
