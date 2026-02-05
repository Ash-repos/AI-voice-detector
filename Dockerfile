# Use full Python 3.11 image
FROM python:3.11

WORKDIR /app

# Install only required system packages
RUN apt-get update --allow-releaseinfo-change \
    && apt-get install -y --no-install-recommends \
       ffmpeg \
       libsndfile1 \
       git \
       curl \
       ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip install --upgrade pip

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Expose port for Cloud Run
EXPOSE 8080

# Run FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
