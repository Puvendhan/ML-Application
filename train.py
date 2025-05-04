# train.py
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
import joblib
import os
import gcsfs

MODEL_VERSION = "1.0.0"
LOCAL_PATH = f"artifacts/{MODEL_VERSION}/model_pipeline.joblib"
GCS_PATH = f"gs://ml-models-iris/{MODEL_VERSION}/model_pipeline.joblib"

# Load and split dataset
X, y = load_iris(return_X_y=True)
X_train, _, y_train, _ = train_test_split(X, y, test_size=0.2)

# Build pipeline
pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('model', LogisticRegression(max_iter=200))
])
pipeline.fit(X_train, y_train)

# Save locally
os.makedirs(os.path.dirname(LOCAL_PATH), exist_ok=True)
joblib.dump(pipeline, LOCAL_PATH)

# Upload to GCS
fs = gcsfs.GCSFileSystem()
with fs.open(GCS_PATH, 'wb') as f:
    joblib.dump(pipeline, f)

print(f"Model pipeline uploaded to {GCS_PATH}")