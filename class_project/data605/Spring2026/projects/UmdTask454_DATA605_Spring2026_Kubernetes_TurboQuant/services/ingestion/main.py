import io
import os

import numpy as np
import onnxruntime as ort
from fastapi import FastAPI, File, HTTPException, UploadFile
from PIL import Image
from prometheus_fastapi_instrumentator import Instrumentator

CLIP_MEAN = np.array([0.48145466, 0.4578275, 0.40821073], dtype=np.float32)
CLIP_STD = np.array([0.26862954, 0.26130258, 0.27577711], dtype=np.float32)
MODEL_PATH = os.environ.get("CLIP_MODEL_PATH", "/app/clip_visual.onnx")

app = FastAPI(title="TurboQuant Ingestion")
session = ort.InferenceSession(MODEL_PATH, providers=["CPUExecutionProvider"])
Instrumentator().instrument(app).expose(app)


def preprocess(image):
    image = image.convert("RGB").resize((224, 224), Image.BICUBIC)
    arr = np.asarray(image, dtype=np.float32) / 255.0
    arr = (arr - CLIP_MEAN) / CLIP_STD
    return arr.transpose(2, 0, 1)[None, :]


@app.get("/healthz")
def healthz():
    return {"status": "ok"}


@app.post("/embed")
async def embed(file: UploadFile = File(...)):
    try:
        img = Image.open(io.BytesIO(await file.read()))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"invalid image: {e}")

    x = preprocess(img)
    feats = session.run(None, {"image": x})[0]
    feats /= np.linalg.norm(feats, axis=1, keepdims=True) + 1e-12
    return {"embedding": feats[0].tolist()}
