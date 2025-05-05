# tests/unit/test_api.py
from unittest import mock
from app import main
import numpy as np

def test_class_names():
    assert main.class_names == ['setosa', 'versicolor', 'virginica']

@mock.patch("app.main.pipeline")
def test_predict_logic():
    main.app.state.pipeline = mock.Mock()
    main.app.state.pipeline.predict.return_value = [1]

    input_data = main.IrisInput(sepal_length=5.1, sepal_width=3.5,
                                 petal_length=1.4, petal_width=0.2)

    response = main.predict(input_data)

    assert response["prediction"] == 1
    assert response["prediction_label"] == "versicolor"
    assert "request_id" in response
