FROM ubuntu:24.04
ENV DEBIAN_FRONTEND noninteractive

# Install system utilities and Python in a single layer.
RUN apt-get update && \
  apt-get upgrade -y && \
  apt-get install -y --no-install-recommends \
    sudo \
    curl \
    git \
    build-essential \
    python3 \
    python3-pip \
    python3-dev \
    python3-venv \
    libgomp1 \
    g++ \
  && rm -rf /var/lib/apt/lists/*

# Install uv for package management.
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:$PATH"

# Install project specific packages using uv.
COPY pyproject.toml uv.lock /app/
WORKDIR /app
RUN uv sync
ENV PATH="/app/.venv/bin:$PATH"

# Install Jupyter.
RUN pip install --upgrade pip && \
    pip install --no-cache-dir jupyterlab jupyterlab_vim jupytext

# Copy project files.
COPY . /app

RUN mkdir /install

# Config.
COPY etc_sudoers /install/
COPY etc_sudoers /etc/sudoers
COPY bashrc /root/.bashrc

# Report package versions.
COPY version.sh /install/
RUN /install/version.sh 2>&1 | tee version.log

# Jupyter.
EXPOSE 8888
