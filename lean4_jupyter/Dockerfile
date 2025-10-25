FROM ubuntu:22.04

# Avoid interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    python3 \
    python3-pip \
    build-essential \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Install elan (Lean version manager)
RUN curl https://raw.githubusercontent.com/leanprover/elan/master/elan-init.sh -sSf | sh -s -- -y --default-toolchain leanprover/lean4:stable
ENV PATH="/root/.elan/bin:${PATH}"

# Install Jupyter
RUN pip3 install --no-cache-dir jupyter notebook jupyterlab

# Install the Lean4 Jupyter kernel (repl)
RUN git clone https://github.com/leanprover-community/repl.git /opt/repl && \
    cd /opt/repl && \
    lake build

# Install the kernel manually
RUN mkdir -p /root/.local/share/jupyter/kernels/lean4 && \
    echo '{\n\
  "display_name": "Lean 4",\n\
  "language": "lean4",\n\
  "argv": ["/opt/repl/.lake/build/bin/repl", "--json"]\n\
}' > /root/.local/share/jupyter/kernels/lean4/kernel.json

# Create a working directory for notebooks
WORKDIR /workspace

# Expose Jupyter port
EXPOSE 8888

# Start Jupyter notebook
CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root", "--NotebookApp.token=''", "--NotebookApp.password=''"]
