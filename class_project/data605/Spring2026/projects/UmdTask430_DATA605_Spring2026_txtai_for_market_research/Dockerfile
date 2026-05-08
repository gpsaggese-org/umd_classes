# txtai Market Research Platform - Docker Configuration

FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PIP_NO_CACHE_DIR=1

# Install system dependencies (curl for healthchecks).
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create data directory for txtai index
RUN mkdir -p /app/data

# Expose API and Streamlit ports.
EXPOSE 8000 8501

# Set environment variable for data directory.
ENV TXTAI_DATA_DIR=/app/data

# Default command runs the FastAPI server; docker-compose overrides this for
# the Streamlit UI service.
CMD ["uvicorn", "app.api.server:app", "--host", "0.0.0.0", "--port", "8000"]
