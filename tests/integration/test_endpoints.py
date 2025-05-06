# tests/integration/test_endpoints.py
from fastapi.testclient import TestClient # type: ignore
from app.main import app

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
    assert "prediction" in body
    assert "prediction_label" in body
    assert "request_id" in body