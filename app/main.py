from fastapi import FastAPI
from pydantic import BaseModel
from uuid import uuid4
import joblib
import numpy as np
import os
from google.cloud import storage

app = FastAPI(title="Iris Classifier")

# Environment variables for model path
model_version = os.getenv("MODEL_VERSION", "1.0.0")
gcs_bucket = os.getenv("GCS_BUCKET", "ml-models-iris")
gcs_model_path = f"{model_version}/model_pipeline.joblib"
local_model_path = f"/tmp/model_pipeline_{model_version}.joblib"

# Class names for species labels
class_names = ['setosa', 'versicolor', 'virginica']

# Function to download the model from GCS
def download_model_from_gcs():
    if os.path.exists(local_model_path):
        return  # If model already exists locally, no need to download again

    # Create a Google Cloud Storage client and download the model file
    client = storage.Client()
    bucket = client.bucket(gcs_bucket)
    blob = bucket.blob(gcs_model_path)

    # Create the local directory if it doesn't exist
    os.makedirs(os.path.dirname(local_model_path), exist_ok=True)
    blob.download_to_filename(local_model_path)
    print(f"Downloaded model to {local_model_path}")

# Load the model
download_model_from_gcs()
pipeline = joblib.load(local_model_path)

# Define the input schema
class IrisInput(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float

@app.post("/predict")
def predict(input_data: IrisInput):
    features = np.array([[input_data.sepal_length, input_data.sepal_width,
                          input_data.petal_length, input_data.petal_width]])

    # Predict the class index
    prediction = pipeline.predict(features)[0]
    
    # Get the class label using the prediction index
    prediction_label = class_names[int(prediction)]

    response = {
        "prediction": int(prediction),
        "prediction_label": prediction_label,
        "request_id": str(uuid4()),
        "model_version": model_version
    }
    return response

# Health check route
@app.get("/health")
def health_check():
    # You can add any logic for your health check here
    return {"status": "healthy"}

# Readiness check route
@app.get("/ready")
def readiness_check():
    # Check if the model is loaded and ready to serve predictions
    if os.path.exists(local_model_path):
        return {"status": "ready"}
    else:
        return {"status": "not ready"}, 503