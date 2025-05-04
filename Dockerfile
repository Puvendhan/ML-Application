# Stage 1: Builder
FROM python:3.9-slim AS build

WORKDIR /app

RUN apt-get update && apt-get install -y gcc && apt-get clean

COPY requirements.txt .
RUN pip install --cache-dir=/cache -r requirements.txt

COPY app/* .

# Stage 2: Final image
FROM python:3.9-slim

WORKDIR /app

# Optional: copy pip cache if you want to reuse it
COPY --from=build /cache /root/.cache/pip

# Copy app code
COPY app/* .
COPY requirements.txt .

# Install only runtime dependencies (fast due to cache)
RUN pip install --cache-dir=/root/.cache/pip -r requirements.txt

ENV MODEL_VERSION=1.0.0
ENV GCS_BUCKET=ml-models-iris

EXPOSE 8000

CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port 8000 & sleep 3600"]