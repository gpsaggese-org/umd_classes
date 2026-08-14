FROM python:3.12-slim

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
        ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /work
COPY requirements.txt /tmp/requirements.txt

# Install CPU-only torch + torchvision together so versions match
# (open_clip pulls torchvision; default index would yield a CUDA-built one).
RUN pip install --no-cache-dir torch torchvision --index-url https://download.pytorch.org/whl/cpu \
    && pip install --no-cache-dir jupyterlab -r /tmp/requirements.txt

EXPOSE 8888
CMD ["jupyter", "lab", \
     "--ip=0.0.0.0", "--port=8888", \
     "--no-browser", "--allow-root", \
     "--ServerApp.token=", "--ServerApp.password=", \
     "--ServerApp.root_dir=/work"]
