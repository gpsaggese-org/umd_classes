FROM python:3.12-slim

ENV DEBIAN_FRONTEND=noninteractive
ENV PATH="/opt/venv/bin:$PATH"

# Install build + runtime deps
RUN apt-get update && apt-get install -y \
    ca-certificates \
    build-essential \
    curl \
    sudo \
    gnupg \
    git \
    vim \
    libgl1 \
    libglib2.0-0 \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN curl -Ls https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:$PATH"

# Create virtual environment and install dependencies via uv
RUN uv venv /opt/venv
COPY requirements.txt /install/requirements.txt
RUN uv pip install --python /opt/venv/bin/python --no-cache -r /install/requirements.txt jupyterlab jupyterlab_vim

# Copy workspace and configs
COPY . /workspace/
RUN mkdir -p /install
COPY etc_sudoers /etc/sudoers
COPY bashrc /root/.bashrc
COPY version.sh /install/version.sh

# Run version report
RUN /install/version.sh 2>&1 | tee version.log

WORKDIR /workspace
EXPOSE 8888