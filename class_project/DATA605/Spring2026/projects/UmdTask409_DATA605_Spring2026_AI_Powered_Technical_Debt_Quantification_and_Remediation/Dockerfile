FROM ubuntu:24.04
ENV DEBIAN_FRONTEND noninteractive

RUN apt-get -y update
RUN apt-get -y upgrade

# Install system utilities.
RUN apt install -y --no-install-recommends \
    sudo \
    curl \
    systemctl \
    gnupg \
    git \
    vim

# Install Python and build deps (venv requires python3-venv on Debian/Ubuntu).
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    python3 \
    python3-pip \
    python3-dev \
    python3-venv \
    && rm -rf /var/lib/apt/lists/*

# Create virtual environment.
RUN python3 -m venv /venv

# Make the venv the default Python.
ENV PATH="/venv/bin:$PATH"

# Upgrade pip inside the venv.
RUN python -m pip install --upgrade pip

# Install uv, if needed.
#RUN curl -LsSf https://astral.sh/uv/install.sh | sh
#ENV PATH="/root/.local/bin:$PATH"
#COPY pyproject.toml uv.lock /app/
#RUN uv sync
    
# Install Jupyter.
RUN pip3 install jupyterlab

# Install Java 17 (needed for PMD and Maven; the pipeline produces refactorings
# that are validated by compiling with javac via Maven).
RUN apt-get update && apt-get install -y --no-install-recommends \
    openjdk-17-jdk-headless \
    && rm -rf /var/lib/apt/lists/*

# Install Maven 3.8.7 (needed for Stage 7 to compile and test refactored code
# in real Java repositories).
RUN apt-get update && apt-get install -y --no-install-recommends \
    maven \
    && rm -rf /var/lib/apt/lists/*

# Install PMD 7.23.0 (used by Stage 2 to find technical debt issues in Java
# source). PMD is not in apt; download the binary release.
RUN apt-get update && apt-get install -y --no-install-recommends \
    unzip \
    wget \
    && rm -rf /var/lib/apt/lists/*
RUN cd /opt && \
    wget -q https://github.com/pmd/pmd/releases/download/pmd_releases%2F7.23.0/pmd-dist-7.23.0-bin.zip && \
    unzip -q pmd-dist-7.23.0-bin.zip && \
    rm pmd-dist-7.23.0-bin.zip
ENV PATH="/opt/pmd-bin-7.23.0/bin:$PATH"

# Install project specific packages.
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

RUN mkdir /install

# Config.
ADD etc_sudoers /install/
COPY etc_sudoers /etc/sudoers
COPY bashrc /root/.bashrc

# Report package versions.
ADD version.sh /install/
RUN /install/version.sh 2>&1 | tee version.log

# Jupyter.
EXPOSE 8888
