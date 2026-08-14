FROM python:3.11-slim

ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies.
# Java JDK (not just JRE) is required by PyFlink because the pemja C extension
# needs JNI headers at compile time. gcc and build-essential are needed to
# compile the native extension.
RUN apt-get update && apt-get install -y \
    ca-certificates \
    default-jdk-headless \
    gcc \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

ENV JAVA_HOME=/usr/lib/jvm/default-java

RUN mkdir -p /install
COPY requirements.txt /install/requirements.txt
RUN pip install --upgrade pip && \
    pip install --no-cache-dir jupyterlab jupyterlab_vim jupytext -r /install/requirements.txt

COPY etc_sudoers /install/
COPY etc_sudoers /etc/sudoers
COPY bashrc /root/.bashrc

COPY version.sh /install/
RUN /install/version.sh 2>&1 | tee /install/version.log

EXPOSE 8888

CMD ["/bin/bash"]
