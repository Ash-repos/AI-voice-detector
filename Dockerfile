FROM python:3.11

WORKDIR /app

# Install system dependencies
RUN apt-get update --allow-releaseinfo-change \
    && apt-get install -y --no-install-recommends \
       ffmpeg \
       libsndfile1 \
       build-essential \
       libatlas-base-dev \
       git \
       wget \
       curl \
       ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip install --upgrade pip

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

EXPOSE 8080
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
