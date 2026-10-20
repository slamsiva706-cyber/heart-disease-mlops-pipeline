# Proposal

## Why

This is a greenfield MLOps course assignment (50 marks) requiring an end-to-end, production-style ML
pipeline for the Heart Disease UCI dataset: data prep through EDA, model training with experiment
tracking, CI/CD, containerized serving, Kubernetes deployment, and monitoring. No pipeline exists yet in
this repository, and the graded deliverables depend on each stage being reproducible and demonstrable
(screenshots, a report, a demo video).

## What Changes

- Add a data acquisition + EDA pipeline for the UCI Heart Disease dataset (download script, cleaning,
  missing-value handling, encoding, visualizations).
- Add a feature engineering and model training pipeline producing at least two classifiers (Logistic
  Regression, Random Forest) with cross-validation and standard classification metrics.
- Add MLflow-based experiment tracking (params, metrics, artifacts, plots) for all training runs.
- Add reproducible model packaging: a saved model + preprocessing pipeline, pinned `requirements.txt`.
- Add a FastAPI model-serving API exposing `POST /predict` (JSON in, prediction + confidence out).
- Add a Dockerfile to containerize the serving API, buildable/runnable locally with a sample request.
- Add a GitHub Actions CI/CD pipeline: lint -> pytest unit tests -> model training, with per-run logs/
  artifacts, failing the pipeline on code or test errors.
- Add Kubernetes deployment manifests targeting local Kubernetes (Minikube/Docker Desktop): Deployment,
  Service, and Ingress/LoadBalancer exposing the API.
- Add request logging and a Prometheus + Grafana monitoring stack (metrics scraping + dashboard) for the
  deployed API.
- Add unit tests (pytest) for data processing and model code.
- Add a written report (setup, EDA/modelling choices, tracking summary, architecture diagram, CI/CD and
  deployment screenshots, repo link) plus a short demo video, as final deliverables (not a spec'd system
  capability).

## Capabilities

### New Capabilities

- `data-pipeline`: Acquiring, cleaning, preprocessing, and exploring the Heart Disease UCI dataset
  (download, missing-value/encoding handling, EDA visualizations) to produce a clean, modeling-ready
  dataset.
- `model-training`: Feature engineering, training/tuning at least two classifiers, cross-validated
  evaluation, MLflow experiment tracking, and reproducible model/preprocessing packaging.
- `model-serving-api`: A FastAPI application exposing `/predict` that loads the packaged model and
  preprocessing pipeline and returns a prediction and confidence score for JSON input, containerized via
  Docker.
- `ci-cd-pipeline`: Automated GitHub Actions workflow that lints, runs unit tests, and runs model training
  on each push/PR, failing fast on errors and preserving per-run logs/artifacts.
- `deployment`: Kubernetes deployment manifests (Deployment, Service, Ingress/LoadBalancer) that run the
  containerized serving API on local Kubernetes (Minikube/Docker Desktop).
- `monitoring`: Request logging plus a Prometheus + Grafana stack that scrapes and visualizes API metrics
  (latency, request/error counts, prediction distribution) for the deployed service.

### Modified Capabilities

(none - no existing specs in this project)

## Impact

- New repository structure: `data/` (raw/processed + download script), `notebooks/` or `scripts/` (EDA,
  training, inference), `src/` (preprocessing, training, serving code), `tests/` (pytest suite),
  `Dockerfile`, `.github/workflows/ci.yml`, `k8s/` (manifests), `monitoring/` (Prometheus/Grafana config),
  `mlruns/`/MLflow tracking store, `requirements.txt`, and a final report + screenshots folder.
- New runtime dependencies: scikit-learn, pandas, MLflow, FastAPI, uvicorn, pytest, Docker, kubectl +
  Minikube, Prometheus, Grafana.
- No existing code or specs are affected; this is additive, greenfield work.
