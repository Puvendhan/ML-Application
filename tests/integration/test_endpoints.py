from fastapi.testclient import TestClient
from app.main import app, get_model
from unittest.mock import Mock

# Use a dummy model for integration
mock_model = Mock()
mock_model.predict.return_value = [2]  # maps to "virginica"

# Override dependency
app.dependency_overrides[get_model] = lambda: mock_model
client = TestClient(app)

def test_predict_endpoint():
    dummy_input = {
        "sepal_length": 6.0,
        "sepal_width": 3.0,
        "petal_length": 4.8,
        "petal_width": 1.8
    }
    response = client.post("/predict", json=dummy_input)

    assert response.status_code == 200
    body = response.json()
    assert body["prediction"] == 2
    assert body["prediction_label"] == "virginica"
    assert "request_id" in body
    assert "model_version" in body
