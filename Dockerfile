# Use full Python image to avoid slim image apt-get issues
FROM python:3.11

# Set working directory
WORKDIR /app

# Install only necessary system packages
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

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

# Expose the port Cloud Run expects
EXPOSE 8080

# Start FastAPI with uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
