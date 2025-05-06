from fastapi import FastAPI, Depends
from pydantic import BaseModel
from uuid import uuid4
import joblib
import numpy as np
import os
import logging
from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_client import Counter

app = FastAPI(title="Iris Classifier")

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("iris-classifier")

# Prometheus metrics
prediction_counter = Counter(
    "iris_predictions_total", "Total number of predictions", ["model_version", "prediction_label"]
)

# Instrumentator for request metrics
Instrumentator().instrument(app).expose(app)

# Environment variables
model_version = os.getenv("MODEL_VERSION", "1.0.0")
gcs_bucket = os.getenv("GCS_BUCKET", "ml-models-iris")
gcs_model_path = f"{model_version}/model_pipeline.joblib"
local_model_path = f"/tmp/model_pipeline_{model_version}.joblib"
class_names = ['setosa', 'versicolor', 'virginica']

@app.on_event("startup")
def startup_event():
    if os.getenv("ENV") != "test":
        model_path = f"/models/model_pipeline.joblib"
        app.state.pipeline = joblib.load(model_path)

class IrisInput(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float


def get_model():
    return app.state.pipeline


@app.post("/predict")
def predict(input_data: IrisInput, model=Depends(get_model)):
    features = np.array([[input_data.sepal_length, input_data.sepal_width,
                          input_data.petal_length, input_data.petal_width]])
    prediction = model.predict(features)[0]
    prediction_label = class_names[int(prediction)]

    request_id = str(uuid4())
    logger.info(f"Request ID: {request_id} | Prediction: {prediction_label}")
    prediction_counter.labels(model_version=model_version, prediction_label=prediction_label).inc()

    return {
        "prediction": int(prediction),
        "prediction_label": prediction_label,
        "request_id": request_id,
        "model_version": model_version
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.get("/ready")
def readiness_check():
    if os.path.exists(local_model_path):
        return {"status": "ready"}
    else:
        return {"status": "not ready"}, 503
