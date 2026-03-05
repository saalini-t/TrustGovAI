# Use Python 3.11 slim image as base
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install additional dependencies for deployment
RUN pip install --no-cache-dir \
    deep-translator \
    gtts \
    python-multipart \
    imageio-ffmpeg

# Copy the entire application
COPY . .

# Create necessary directories
RUN mkdir -p audio_cache data/schemes_docs

# Expose port 8000 for the API
EXPOSE 8000

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV FAST_MODE=true
ENV PORT=8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/ || exit 1

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
