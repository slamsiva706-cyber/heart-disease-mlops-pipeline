# Spec Delta

## Purpose

Trains, tunes, evaluates, and tracks at least two classification models on the prepared heart disease
dataset, and packages the resulting model and preprocessing pipeline for reproducible reuse.

## ADDED Requirements

### Requirement: Feature Engineering Pipeline
The system SHALL apply a documented, reusable scaling/encoding pipeline to transform cleaned data into
final model-ready features.

#### Scenario: Consistent feature transform
- **WHEN** the feature engineering pipeline is applied to the cleaned dataset
- **THEN** it outputs a feature matrix with scaled numeric features and encoded categorical features,
  reusable for both training and inference

### Requirement: Multi-Model Training and Evaluation
The system SHALL train and evaluate at least two distinct classification algorithms (Logistic Regression
and Random Forest) using cross-validation and report accuracy, precision, recall, and ROC-AUC for each.

#### Scenario: Two models trained and scored
- **WHEN** the training step runs on the engineered features
- **THEN** both a Logistic Regression model and a Random Forest model are trained and each has
  cross-validated accuracy, precision, recall, and ROC-AUC recorded

### Requirement: Experiment Tracking
The system SHALL log parameters, metrics, and artifacts (including plots) for every training run to an
experiment tracking tool.

#### Scenario: Run logged with artifacts
- **WHEN** a model training run completes
- **THEN** its parameters, metrics, and output artifacts/plots are recorded under a retrievable experiment
  run ID

### Requirement: Reproducible Model Packaging
The system SHALL save the selected final model together with its preprocessing pipeline/transformers in a
reusable serialized format, alongside a pinned dependency manifest, such that the model can be reloaded and
produce identical predictions in a new environment.

#### Scenario: Model reload produces consistent predictions
- **WHEN** the packaged model and preprocessing pipeline are loaded in a fresh environment using the
  pinned dependencies
- **THEN** predictions on the same input match the predictions produced at training time
