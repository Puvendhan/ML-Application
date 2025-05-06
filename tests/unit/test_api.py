from unittest import mock
from app import main

def test_class_names():
    assert main.class_names == ['setosa', 'versicolor', 'virginica']

def test_predict_logic():
    mock_pipeline = mock.Mock()
    mock_pipeline.predict.return_value = [1]

    # Use dependency injection to pass mocked model
    with mock.patch("app.main.get_model", return_value=mock_pipeline):
        input_data = main.IrisInput(sepal_length=5.1, sepal_width=3.5,
                                    petal_length=1.4, petal_width=0.2)
        response = main.predict(input_data)

    assert response["prediction"] == 1
    assert response["prediction_label"] == "versicolor"
    assert "request_id" in response
