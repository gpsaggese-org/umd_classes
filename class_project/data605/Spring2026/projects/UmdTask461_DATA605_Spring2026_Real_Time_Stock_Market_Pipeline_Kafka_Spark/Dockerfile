FROM python:3.11-slim

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    default-jdk \
    curl \
    vim \
    && rm -rf /var/lib/apt/lists/*

ENV JAVA_HOME=/usr/lib/jvm/default-java
ENV PATH="${JAVA_HOME}/bin:${PATH}"

RUN pip install --upgrade pip
RUN pip install jupyterlab jupyterlab_vim

COPY requirements.txt /install/requirements.txt
RUN pip install --no-cache-dir -r /install/requirements.txt

WORKDIR /app
COPY . /app

EXPOSE 8888

CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root", "--NotebookApp.token=''", "--NotebookApp.password=''"]
