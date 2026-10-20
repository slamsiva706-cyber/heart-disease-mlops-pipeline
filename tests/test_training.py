import joblib
import numpy as np
import pandas as pd

from src.features.pipeline import FEATURE_COLUMNS, build_feature_pipeline
from src.training.train import train


def _sample_dataframe(n: int = 20) -> pd.DataFrame:
    rng = np.random.default_rng(42)
    data = {
        "age": rng.integers(29, 77, n).astype(float),
        "trestbps": rng.integers(94, 200, n).astype(float),
        "chol": rng.integers(126, 564, n).astype(float),
        "thalach": rng.integers(71, 202, n).astype(float),
        "oldpeak": rng.uniform(0, 6.2, n),
        "sex": rng.integers(0, 2, n).astype(float),
        "fbs": rng.integers(0, 2, n).astype(float),
        "exang": rng.integers(0, 2, n).astype(float),
        "cp": rng.integers(1, 5, n).astype(float),
        "restecg": rng.integers(0, 3, n).astype(float),
        "slope": rng.integers(1, 4, n).astype(float),
        "ca": rng.integers(0, 4, n).astype(float),
        "thal": rng.choice([3, 6, 7], n).astype(float),
        "target": rng.integers(0, 2, n),
    }
    return pd.DataFrame(data)


def test_feature_pipeline_output_shape_and_dtype():
    df = _sample_dataframe()
    X = df[FEATURE_COLUMNS]

    pipeline = build_feature_pipeline()
    transformed = pipeline.fit_transform(X)

    assert transformed.shape[0] == len(X)
    assert transformed.shape[1] > len(FEATURE_COLUMNS)  # one-hot expands categorical columns
    assert np.issubdtype(transformed.dtype, np.floating)


def test_train_saves_reloadable_model_with_consistent_predictions(tmp_path):
    df = _sample_dataframe(n=60)
    data_path = tmp_path / "data.csv"
    df.to_csv(data_path, index=False)
    model_dir = tmp_path / "models"

    results, best_name, model_path = train(data_path=data_path, model_dir=model_dir, cv_folds=3)

    assert best_name in results
    assert model_path.exists()

    reloaded = joblib.load(model_path)
    X = df[FEATURE_COLUMNS]
    original_preds = joblib.load(model_path).predict(X)
    reloaded_preds = reloaded.predict(X)

    assert np.array_equal(original_preds, reloaded_preds)
