FROM python:3.12-slim

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    git \
    build-essential \
    g++ \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /install
COPY project_files/requirements.txt /install/requirements.txt
RUN pip install --upgrade pip && \
    pip install --no-cache-dir \
        jupyterlab \
        jupyterlab_vim \
        jupytext \
        -r /install/requirements.txt

COPY etc_sudoers /etc/sudoers
COPY bashrc      /root/.bashrc

# Version report 
COPY version.sh /install/version.sh
RUN chmod +x /install/version.sh && \
    /install/version.sh 2>&1 | tee /install/version.log

# Working directory 
WORKDIR /app

# HuggingFace cache dir 
ENV HF_HOME=/hf_cache
ENV TRANSFORMERS_CACHE=/hf_cache

#  Jupyter port 
EXPOSE 8888

CMD ["/bin/bash"]
