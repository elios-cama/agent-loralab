FROM python:3.10-slim

WORKDIR /app

# Install only required system packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies with no cache
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PORT=8000

# Expose port
EXPOSE 8000

# Default command - can be overridden by railway.json startCommand
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"] 