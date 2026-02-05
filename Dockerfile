# Use full Python image to avoid slim image apt-get issues
FROM python:3.11

# Set working directory
WORKDIR /app

# Install only the necessary system dependencies
RUN apt-get update --allow-releaseinfo-change \
    && apt-get install -y --no-install-recommends \
       ffmpeg \
       libsndfile1 \
       git \
       wget \
       curl \
       ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip install --upgrade pip

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project files
COPY . .

# Expose the port for Cloud Run
EXPOSE 8080

# Start the FastAPI app with uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
