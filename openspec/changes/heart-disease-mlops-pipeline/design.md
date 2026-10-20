# Design

## Context

Greenfield repository (only `openspec/` scaffolding and a PDF exist today). No cloud account is available,
so deployment targets local Kubernetes rather than a managed cloud K8s service. See proposal.md - Why.

Key environment facts:
- `git` is not currently on PATH on the dev machine; must be installed before pushing to GitHub (required
  for the CI/CD and repo deliverables).
- Python 3.14 is available via the `py` launcher.

## Goals / Non-Goals

**Goals:**
- Define a repo layout and tool stack that lets every capability in the proposal be implemented
  independently and tested locally before CI/CD and deployment are wired up.
- Keep the stack runnable entirely offline/locally (no paid cloud dependency) while still satisfying every
  graded assignment requirement.

**Non-Goals:**
- Supporting a managed cloud Kubernetes target (GKE/EKS/AKS) - explicitly deferred; local Kubernetes
  (Minikube/Docker Desktop) is the only deployment target this design covers.
- Horizontal scaling, multi-tenant auth, or production-grade security hardening beyond what the assignment
  requires.
- A remote/shared MLflow tracking server - tracking runs locally against the filesystem.

## Decisions

### Repository layout
```
data/                 # download script + raw/processed data (processed data git-ignored if large)
notebooks/            # EDA notebook(s)
src/
  data/               # acquisition + cleaning + preprocessing
  features/           # feature engineering pipeline (shared by training and serving)
  training/           # train.py - trains, cross-validates, logs to MLflow, packages model
  serving/             # FastAPI app: main.py, schemas.py
tests/                # pytest: data, features, training, API
mlruns/                # local MLflow tracking store (git-ignored)
models/                # packaged model + preprocessing pipeline artifact (git-ignored, produced by CI)
Dockerfile
requirements.txt
.github/workflows/ci.yml
k8s/                   # deployment.yaml, service.yaml, ingress.yaml
monitoring/            # prometheus.yaml, grafana dashboard JSON
docs/                  # final report + screenshots
```
Rationale: mirrors the proposal's capability boundaries 1:1 with top-level folders, so each capability's
implementation and tests stay colocated and CI stages map cleanly onto `src/` subfolders.

### Feature pipeline shared between training and serving
The `src/features` scaling/encoding pipeline (scikit-learn `Pipeline`/`ColumnTransformer`) is fit once
during training and serialized alongside the model (e.g., via `joblib` or as part of an MLflow pyfunc
model). The serving API loads this same artifact rather than reimplementing preprocessing, so training and
inference cannot silently drift apart. Alternative considered: duplicate preprocessing code in the API -
rejected because it risks train/serve skew, which the reproducibility requirement explicitly guards
against.

### Experiment tracking: local MLflow
MLflow tracking server runs embedded (`mlruns/` on local filesystem), no separate tracking service to
stand up or secure. Sufficient for a single-contributor assignment; revisit only if multi-user tracking is
ever needed.

### Serving: FastAPI + Uvicorn, single `/predict` endpoint
Pydantic request/response models give input validation (satisfies the "Invalid Input Handling"
requirement) and automatic OpenAPI docs for free, which doubles as API documentation for the report.

### CI/CD: GitHub Actions, three sequential jobs/steps (lint -> test -> train)
Chosen because the deliverable is already a GitHub repo; avoids standing up/maintaining a Jenkins server.
Training is included as a pipeline stage (not just tests) per the assignment's explicit requirement, using
a small/fast config (fewer CV folds or a data subsample) to keep CI runtime reasonable.

### Deployment: local Kubernetes (Minikube/Docker Desktop)
Chosen because no cloud account exists yet and acquiring one adds signup/billing friction and risk without
changing what's demonstrated. Deployment + Service + Ingress (or a NodePort/LoadBalancer via
`minikube tunnel`) are functionally equivalent to a cloud setup for grading purposes, per the assignment's
own alternative.

### Monitoring: Prometheus + Grafana in-cluster
A `prometheus-fastapi-instrumentator` (or equivalent) exposes a `/metrics` endpoint on the serving API;
Prometheus (deployed in the same Minikube cluster) scrapes it, and Grafana visualizes it. Chosen over a
simpler logs-only dashboard because the user opted for the more production-representative stack despite
the lower mark weight.

## Risks / Trade-offs

- [Local-only deployment may look less "production" than a public cloud URL for grading] → Mitigate with
  thorough screenshots/video showing the full local deployment and explicitly note in the report that
  Minikube is an assignment-sanctioned alternative to cloud K8s.
- [Training inside CI could be slow or flaky on shared GitHub-hosted runners] → Use a reduced CI training
  config (fewer folds/estimators or a sampled dataset) distinct from the full local training run used for
  the final packaged model.
- [`git` not yet installed/on PATH] → Must be resolved before any GitHub push; first implementation task
  should verify/install Git.
- [Prometheus + Grafana adds operational surface (two more Deployments/Services in Minikube)] → Keep
  manifests minimal (single replica each, default scrape config) since this is a demo, not HA monitoring.

## Migration Plan

Greenfield build, so "migration" is really sequencing:
1. Data pipeline -> 2. Model training (+ MLflow + packaging) -> 3. Serving API -> 4. Containerize ->
5. CI/CD -> 6. K8s deployment -> 7. Monitoring -> 8. Report/video.
No rollback needed beyond reverting commits; nothing in this change replaces an existing running system.
