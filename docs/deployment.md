# Deployment & Operations Guide

This guide details the deployment options for **AgentOps Nexus** from local developer environments to staging/production Kubernetes environments.

---

## 1. Local Deployment (Docker Compose)

The simplest way to run the entire system is using Docker Compose:

```bash
# Start all developer containers
docker-compose -f docker-compose.dev.yml up -build
```

### Port Mapping Summary
*   **Next.js Frontend**: `http://localhost:3000`
*   **FastAPI Backend**: `http://localhost:8000/api/docs` (Swagger docs)
*   **Qdrant Console**: `http://localhost:6333/dashboard`
*   **Grafana Dashboard**: `http://localhost:3001` (Creds: `admin` / `admin`)
*   **Prometheus Target Scraper**: `http://localhost:9090`

---

## 2. Production Deployment (Kubernetes)

To deploy the production-ready monorepo onto a Kubernetes cluster (e.g. AWS EKS, GKE):

### Step 1: Deploy Core Database & Services
```bash
kubectl apply -f infra/k8s/deployment.yaml
```

This deploys:
*   PostgreSQL 16 pods with persistent volumes.
*   Redis cache pods for celery queue and rate limiter.
*   Qdrant vector engine cluster.

### Step 2: Configure Environment Secret values
Create the `agentops-secrets` to store API keys securely:
```bash
kubectl create secret generic agentops-secrets \
  --from-literal=SECRET_KEY="supersecretkey..." \
  --from-literal=OPENAI_API_KEY="sk-..." \
  --from-literal=ENKRYPT_API_KEY="yourkey..." \
  --namespace=agentops-nexus
```

### Step 3: Verify Pod Health Status
```bash
kubectl get pods -n agentops-nexus
```
Make sure all microservice pods are running.
