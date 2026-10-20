"""FastAPI serving application for the heart disease risk model."""
import logging
import time
from pathlib import Path

import joblib
import pandas as pd
from fastapi import FastAPI, Request

from src.features.pipeline import FEATURE_COLUMNS
from src.serving.schemas import PredictionRequest, PredictionResponse

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_MODEL_PATH = REPO_ROOT / "models" / "model.joblib"

logger = logging.getLogger("heart_disease_api")
logging.basicConfig(level=logging.INFO)

app = FastAPI(title="Heart Disease Risk API")

_model = None


def get_model():
    """Lazily load and cache the packaged model + preprocessing pipeline."""
    global _model
    if _model is None:
        _model = joblib.load(DEFAULT_MODEL_PATH)
    return _model


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    latency_ms = (time.perf_counter() - start) * 1000
    logger.info(
        "request method=%s path=%s status=%s latency_ms=%.2f",
        request.method, request.url.path, response.status_code, latency_ms,
    )
    return response


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict", response_model=PredictionResponse)
def predict(payload: PredictionRequest) -> PredictionResponse:
    model = get_model()
    row = pd.DataFrame([payload.model_dump()])[FEATURE_COLUMNS]
    prediction = int(model.predict(row)[0])
    confidence = float(model.predict_proba(row)[0][prediction])
    return PredictionResponse(prediction=prediction, confidence=confidence)
