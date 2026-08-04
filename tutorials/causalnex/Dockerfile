# Refer to https://github.com/mckinsey/causalnex/blob/develop/devel-cpu.Dockerfile
FROM ubuntu:20.04

# Avoid interactive prompts during apt operations.
ENV DEBIAN_FRONTEND=noninteractive

# Install CA certificates, build tools, and graphviz (needed for pygraphviz).
RUN apt-get update -y && apt-get install -y \
    python3.10 \
    python3-venv \
    python3-pip \
    ca-certificates \
    build-essential \
    graphviz \
    graphviz-dev \
    && rm -rf /var/lib/apt/lists/*

# Create virtual environment.
RUN python3 -m venv /opt/venv

# Make the venv the default Python.
ENV PATH="/opt/venv/bin:$PATH"

RUN mkdir -p /install

# Upgrade pip inside the venv.
RUN python -m pip install --upgrade pip

# Install project specific packages.
COPY requirements.txt /install/requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir jupyterlab jupyterlab_vim jupytext
RUN pip install --no-cache-dir cython
RUN pip install --no-cache-dir -r /install/requirements.txt

RUN mkdir -p /install

# Config.
ADD etc_sudoers /install/
COPY etc_sudoers /etc/sudoers
COPY bashrc /root/.bashrc

# Report package versions.
ADD version.sh /install/
RUN /install/version.sh 2>&1 | tee version.log

# Jupyter.
EXPOSE 8888
