ARG BUILD_ENV="build"

FROM python:3.9-slim AS build
ONBUILD RUN echo "Building the image..."

WORKDIR /app
RUN apt-get update && apt-get install -y gcc && apt-get clean
COPY requirements.txt .
RUN pip install --cache-dir=/cache -r requirements.txt
COPY app/* .

FROM ${BUILD_ENV}

LABEL maintainer="puvendhan" \
      version="0.1"

RUN useradd -m appuser

WORKDIR /app

COPY --from=build /cache /root/.cache/pip
COPY --from=build /app /app

RUN pip install --cache-dir=/root/.cache/pip -r requirements.txt

ENV MODEL_VERSION=1.0.0
ENV GCS_BUCKET=ml-models-iris

USER appuser

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]