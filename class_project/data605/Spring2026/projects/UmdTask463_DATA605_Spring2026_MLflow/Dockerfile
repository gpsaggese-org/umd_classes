# Use Python 3.12 slim
FROM python:3.12-slim

# Avoid interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# Install basic system tools
RUN apt-get update && apt-get install -y \
    ca-certificates \
    curl \
    git \
    sudo \
    && rm -rf /var/lib/apt/lists/*

# Setup directory structure
RUN mkdir -p /install /project
WORKDIR /project

# Install Python packages
COPY requirements.txt /install/requirements.txt
RUN pip install --upgrade pip && \
    pip install --no-cache-dir jupyterlab jupyterlab_vim jupytext mlflow -r /install/requirements.txt

# Config files
COPY etc_sudoers /etc/sudoers
COPY bashrc /root/.bashrc

# Reporting
COPY version.sh /install/
RUN /install/version.sh 2>&1 | tee /install/version.log

# Jupyter and MLflow UI ports
EXPOSE 8888 5000

CMD ["/bin/bash"]
