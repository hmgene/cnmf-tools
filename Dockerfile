# Use an official Python image as the base
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    && rm -rf /var/lib/apt/lists/*

# Install required Python packages
RUN pip install --no-cache-dir \
    fastapi \
    csv \
    logging \
    json \
    pandas \
    pydantic \
    numpy \
    scikit-learn \
    scanpy \
    matplotlib

# Copy application files (optional, if needed)
COPY . .

# Expose FastAPI default port
EXPOSE 8000

# Command to run FastAPI (modify as needed)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
