FROM python:3.11-slim AS builder
WORKDIR /build
RUN pip install --no-cache-dir torch==2.4.0 open-clip-torch==2.26.1 onnx==1.17.0
COPY export_clip.py .
RUN python export_clip.py /build/clip_visual.onnx

FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /build/clip_visual.onnx /app/clip_visual.onnx
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY main.py .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
