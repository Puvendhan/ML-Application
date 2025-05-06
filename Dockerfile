# Stage 1: Builder
FROM python:3.9-slim AS build

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y gcc && apt-get clean

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --cache-dir=/cache -r requirements.txt

# Copy the app source code
COPY app/* .

# Stage 2: Final image
FROM python:3.9-slim

# Create non-root user
RUN useradd -m appuser

WORKDIR /app

# Optional: copy pip cache if you want to reuse it
COPY --from=build /cache /root/.cache/pip

# Copy the app source code
COPY app/* .
COPY requirements.txt .

# Install only runtime dependencies
RUN pip install --cache-dir=/root/.cache/pip -r requirements.txt

# Set environment variables
ENV MODEL_VERSION=1.0.0
ENV GCS_BUCKET=ml-models-iris

# Use non-root user
USER appuser

# Expose the port that the app will run on
EXPOSE 8000

# Use uvicorn to serve the app (removes the need for `sleep`)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]