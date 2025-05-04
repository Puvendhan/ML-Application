# app/model.py
import os
import joblib
import gcsfs

MODEL_VERSION = os.getenv("MODEL_VERSION", "1.0.0")
GCS_PATH = f"gs://ml-models-iris/{MODEL_VERSION}/model_pipeline.joblib"

def load_model():
    fs = gcsfs.GCSFileSystem()
    with fs.open(GCS_PATH, 'rb') as f:
        return joblib.load(f)

model = load_model()