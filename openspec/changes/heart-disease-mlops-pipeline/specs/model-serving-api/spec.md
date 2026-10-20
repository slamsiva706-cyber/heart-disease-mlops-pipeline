# Spec Delta

## Purpose

Serves the packaged heart disease risk model over HTTP via a containerized `/predict` endpoint that
returns predictions with confidence scores.

## ADDED Requirements

### Requirement: Predict Endpoint Contract
The system SHALL expose an HTTP POST /predict endpoint that accepts patient feature data as JSON and
returns a JSON response containing a binary prediction and a confidence score.

#### Scenario: Valid prediction request
- **WHEN** a client sends a POST request to /predict with valid patient feature JSON
- **THEN** the response is JSON containing a prediction (presence/absence of heart disease) and a
  confidence score

### Requirement: Invalid Input Handling
The system SHALL validate incoming request payloads and SHALL return a client error response with a
descriptive message when required fields are missing or malformed, without crashing the service.

#### Scenario: Malformed request rejected
- **WHEN** a client sends a POST request to /predict with missing or invalid fields
- **THEN** the service returns a 4xx error response describing the validation failure and remains
  available for subsequent requests

### Requirement: Containerized Runtime
The system SHALL be packaged as a container image that builds successfully and serves correct /predict
responses when run locally with a sample input, independent of the host's installed dependencies.

#### Scenario: Local container verification
- **WHEN** the container image is built and run locally
- **THEN** sending a sample JSON request to /predict returns a valid prediction response from within the
  running container
