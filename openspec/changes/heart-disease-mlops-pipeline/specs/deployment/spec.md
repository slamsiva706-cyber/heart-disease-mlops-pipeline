# Spec Delta

## Purpose

Runs the containerized model-serving API on a local Kubernetes cluster, reachable through a stable network
entry point.

## ADDED Requirements

### Requirement: Kubernetes Deployment Manifest
The system SHALL provide a Kubernetes Deployment manifest that runs the containerized serving API with a
specified number of replicas and restarts failed pods automatically.

#### Scenario: Deployment applied successfully
- **WHEN** the Deployment manifest is applied to a local Kubernetes cluster (Minikube/Docker Desktop)
- **THEN** the specified number of serving API pods reach a Running/Ready state

### Requirement: Network Exposure
The system SHALL expose the deployed serving API through a Kubernetes Service combined with an Ingress or
LoadBalancer, such that /predict is reachable from outside the pod network using a stable address.

#### Scenario: Endpoint reachable after deployment
- **WHEN** the Service and Ingress/LoadBalancer manifests are applied alongside the Deployment
- **THEN** a client outside the cluster can reach the /predict endpoint through the exposed address and
  receive a valid response
