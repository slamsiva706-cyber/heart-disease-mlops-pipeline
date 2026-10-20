from fastapi.testclient import TestClient

from src.serving import main as main_module

VALID_PAYLOAD = {
    "age": 63, "sex": 1, "cp": 1, "trestbps": 145, "chol": 233,
    "fbs": 1, "restecg": 2, "thalach": 150, "exang": 0,
    "oldpeak": 2.3, "slope": 3, "ca": 0, "thal": 6,
}


class _StubModel:
    def predict(self, X):
        return [1]

    def predict_proba(self, X):
        return [[0.2, 0.8]]


def test_predict_returns_prediction_and_confidence(monkeypatch):
    monkeypatch.setattr(main_module, "get_model", lambda: _StubModel())
    client = TestClient(main_module.app)

    response = client.post("/predict", json=VALID_PAYLOAD)

    assert response.status_code == 200
    body = response.json()
    assert body["prediction"] == 1
    assert body["confidence"] == 0.8


def test_predict_rejects_missing_field(monkeypatch):
    monkeypatch.setattr(main_module, "get_model", lambda: _StubModel())
    client = TestClient(main_module.app)
    bad_payload = dict(VALID_PAYLOAD)
    del bad_payload["age"]

    response = client.post("/predict", json=bad_payload)

    assert response.status_code == 422
    assert "age" in response.text


def test_predict_rejects_out_of_range_binary_field(monkeypatch):
    monkeypatch.setattr(main_module, "get_model", lambda: _StubModel())
    client = TestClient(main_module.app)
    bad_payload = dict(VALID_PAYLOAD, sex=5)

    response = client.post("/predict", json=bad_payload)

    assert response.status_code == 422
