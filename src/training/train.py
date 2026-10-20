"""Trains Logistic Regression and Random Forest classifiers with MLflow tracking.

Run as a script: python -m src.training.train
"""
# ruff: noqa: I001
import argparse
from pathlib import Path

import joblib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import mlflow
import mlflow.sklearn
import pandas as pd
from sklearn.base import clone
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import ConfusionMatrixDisplay, RocCurveDisplay
from sklearn.model_selection import cross_validate, train_test_split
from sklearn.pipeline import Pipeline

from src.features.pipeline import FEATURE_COLUMNS, build_feature_pipeline

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DATA = REPO_ROOT / "data" / "processed" / "heart_disease_clean.csv"
DEFAULT_MODEL_DIR = REPO_ROOT / "models"
SCORING = ["accuracy", "precision", "recall", "roc_auc"]


def _build_models(random_state: int = 42) -> dict:
    return {
        "logistic_regression": LogisticRegression(max_iter=1000, random_state=random_state),
        "random_forest": RandomForestClassifier(n_estimators=200, random_state=random_state),
    }


def _log_evaluation_plots(pipeline: Pipeline, X: pd.DataFrame, y: pd.Series, random_state: int) -> None:
    """Fit on a held-out split and log a confusion matrix + ROC curve as MLflow artifacts."""
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=random_state, stratify=y
    )
    eval_pipeline = clone(pipeline)
    eval_pipeline.fit(X_train, y_train)

    fig, ax = plt.subplots(figsize=(5, 4))
    ConfusionMatrixDisplay.from_estimator(eval_pipeline, X_test, y_test, ax=ax)
    mlflow.log_figure(fig, "confusion_matrix.png")
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(5, 4))
    RocCurveDisplay.from_estimator(eval_pipeline, X_test, y_test, ax=ax)
    mlflow.log_figure(fig, "roc_curve.png")
    plt.close(fig)


def train(
    data_path: Path = DEFAULT_DATA, model_dir: Path = DEFAULT_MODEL_DIR, cv_folds: int = 5
) -> tuple[dict, str, Path]:
    """Train and cross-validate both models, log everything to MLflow, and save the best pipeline."""
    df = pd.read_csv(data_path)
    X = df[FEATURE_COLUMNS]
    y = df["target"]

    mlflow.set_experiment("heart-disease-classification")

    results: dict[str, dict[str, float]] = {}
    best_name, best_pipeline, best_score = None, None, -1.0

    for name, estimator in _build_models().items():
        pipeline = Pipeline([
            ("features", build_feature_pipeline()),
            ("model", estimator),
        ])

        with mlflow.start_run(run_name=name):
            cv_results = cross_validate(pipeline, X, y, cv=cv_folds, scoring=SCORING)
            metrics = {metric: float(cv_results[f"test_{metric}"].mean()) for metric in SCORING}

            mlflow.log_param("model", name)
            mlflow.log_param("cv_folds", cv_folds)
            for metric_name, value in metrics.items():
                mlflow.log_metric(metric_name, value)

            pipeline.fit(X, y)
            mlflow.sklearn.log_model(pipeline, artifact_path="model")
            _log_evaluation_plots(pipeline, X, y, random_state=42)

            results[name] = metrics
            if metrics["roc_auc"] > best_score:
                best_name, best_pipeline, best_score = name, pipeline, metrics["roc_auc"]

    model_dir.mkdir(parents=True, exist_ok=True)
    model_path = model_dir / "model.joblib"
    joblib.dump(best_pipeline, model_path)

    return results, best_name, model_path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, default=DEFAULT_DATA)
    parser.add_argument("--model-dir", type=Path, default=DEFAULT_MODEL_DIR)
    parser.add_argument("--cv-folds", type=int, default=5)
    args = parser.parse_args()

    results, best_name, model_path = train(args.data, args.model_dir, args.cv_folds)
    for name, metrics in results.items():
        print(f"{name}: " + ", ".join(f"{k}={v:.4f}" for k, v in metrics.items()))
    print(f"Best model: {best_name} -> saved to {model_path}")


if __name__ == "__main__":
    main()
