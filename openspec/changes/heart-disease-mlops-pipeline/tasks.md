# Tasks

## 1. Environment & Repo Setup

- [x] 1.1 Install Git and verify `git --version` succeeds; initialize the local repo and create a GitHub remote, verify `git remote -v` shows it
- [x] 1.2 Create the repo layout from design.md (`data/`, `notebooks/`, `src/{data,features,training,serving}`, `tests/`, `k8s/`, `monitoring/`, `docs/`) and verify a directory listing matches
- [x] 1.3 Create `requirements.txt` with pinned core dependencies (pandas, scikit-learn, mlflow, fastapi, uvicorn, pytest, joblib) and verify `pip install -r requirements.txt` succeeds in a clean virtualenv

## 2. Data Pipeline

- [x] 2.1 Write dataset download script (`src/data/download.py`) fetching the UCI Heart Disease CSV, verify running it on a clean environment produces the raw CSV at the documented path
- [x] 2.2 Write cleaning/encoding step (`src/data/clean.py`) handling missing values and encoding categoricals, verify it produces a dataset with zero missing values and numeric dtypes
- [x] 2.3 Write EDA notebook/script producing histograms, correlation heatmap, and class-balance plot, verify the plot files are saved under a documented output folder
- [x] 2.4 Add pytest tests for the download/clean steps in `tests/test_data.py`, verify `pytest tests/test_data.py` passes

## 3. Feature Engineering & Model Training

- [x] 3.1 Implement the shared feature pipeline (`src/features/pipeline.py`) with scaling/encoding via `sklearn.ColumnTransformer`, verify a unit test confirms output shape/dtypes
- [x] 3.2 Implement training script (`src/training/train.py`) training Logistic Regression and Random Forest with cross-validation, verify it reports accuracy, precision, recall, and ROC-AUC for both models
- [x] 3.3 Integrate MLflow tracking (params, metrics, artifacts, plots) into `train.py`, verify `mlruns/` contains a logged run with artifacts after running it
- [x] 3.4 Save the final selected model plus feature pipeline as a packaged, reloadable artifact, verify a reload script produces identical predictions on a held-out sample in a fresh environment using `requirements.txt`
- [x] 3.5 Add pytest tests for the feature pipeline and training code in `tests/test_training.py`, verify `pytest tests/test_training.py` passes

## 4. Model Serving API

- [x] 4.1 Implement the FastAPI app (`src/serving/main.py`) with Pydantic request/response schemas and `POST /predict` loading the packaged model, verify a local `uvicorn` run returns a valid prediction for a sample request
- [x] 4.2 Add input validation returning a 4xx response with a descriptive error on malformed requests, verify a pytest test asserts the error response for an invalid payload
- [x] 4.3 Add API tests using FastAPI's `TestClient` covering valid and invalid requests in `tests/test_api.py`, verify `pytest tests/test_api.py` passes

## 5. Containerization

- [x] 5.1 Write a `Dockerfile` packaging the serving API and its dependencies, verify `docker build` succeeds
- [x] 5.2 Run the built image locally and send a sample `/predict` request, verify the container returns a correct JSON prediction response independent of the host environment

## 6. CI/CD Pipeline

- [x] 6.1 Add lint tooling/config (e.g., ruff or flake8), verify running it locally reports no errors on current code
- [ ] 6.2 Write `.github/workflows/ci.yml` with sequential lint -> pytest -> training stages, verify a pushed commit/PR triggers the workflow and all stages run in order
- [ ] 6.3 Configure the workflow to fail fast on lint/test/training errors and upload logs/artifacts per run, verify an intentionally broken test causes the workflow to fail and the training stage to be skipped, then revert the break

## 7. Production Deployment

- [ ] 7.1 Write `k8s/deployment.yaml` running the containerized API with a defined replica count, verify `kubectl apply -f k8s/deployment.yaml` on Minikube reaches Running/Ready pods
- [ ] 7.2 Write `k8s/service.yaml` and `k8s/ingress.yaml` (or LoadBalancer) exposing the API, verify a request to `/predict` through the exposed address returns a valid response, and capture deployment screenshots
- [ ] 7.3 Document local Kubernetes setup/access instructions in `docs/`, verify following the documented steps from a clean Minikube cluster reproduces a working deployment

## 8. Monitoring & Logging

- [ ] 8.1 Add structured request logging (timestamp, status, latency) to the serving API, verify log output contains these fields for a sample request
- [ ] 8.2 Expose a `/metrics` endpoint (e.g., via `prometheus-fastapi-instrumentator`) and deploy Prometheus in Minikube scraping it, verify the Prometheus targets page shows the API as healthy
- [ ] 8.3 Deploy Grafana and build a dashboard for request count, error rate, and latency, verify the dashboard renders live data from a sample request burst, and capture dashboard screenshots

## 9. Documentation & Reporting

- [ ] 9.1 Write the final report (`docs/report.md`/`.pdf`/`.docx`, max 10 pages) covering setup instructions, EDA/modelling choices, experiment tracking summary, an architecture diagram, and CI/CD + deployment screenshots, verify it includes the repo link and stays within 10 pages
- [ ] 9.2 Record a short demo video walking through the end-to-end pipeline, verify the video file/link is included with the deliverables
- [ ] 9.3 Assemble the final deliverables checklist (code, Dockerfile, requirements, dataset + download script, notebooks/scripts, `tests/`, CI workflow YAML, k8s manifests, screenshots folder, report, video) and verify every item from the assignment's Deliverables list is present in the repo

## Workflow follow-up

- Archive this change once the assignment is submitted and graded artifacts are finalized.
