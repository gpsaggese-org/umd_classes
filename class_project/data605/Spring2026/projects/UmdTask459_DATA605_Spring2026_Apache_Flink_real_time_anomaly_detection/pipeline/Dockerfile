FROM python:3.11-slim

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    ca-certificates \
    default-jdk-headless \
    gcc \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

ENV JAVA_HOME=/usr/lib/jvm/default-java

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip setuptools && \
    pip install --no-cache-dir -r requirements.txt

COPY openweather_stream_job.py .

CMD ["python", "openweather_stream_job.py"]
