# Enterprise Deployment Guide

## Prerequisites
- Docker v24+ & Docker Compose v2.20+
- Python 3.12+
- Node.js v20+ & npm v10+
- Kubernetes cluster v1.28+ (for K8s deployment)

## Local Docker Compose Deployment

```bash
# 1. Clone & Enter repository
cd "Cross-Hospital Diagnosis Model"

# 2. Build and launch all services with Docker Compose
docker-compose -f docker/docker-compose.yml up --build -d

# 3. Access Services:
# - Enterprise React Dashboard: http://localhost:3000
# - FastAPI Aggregator Swagger Docs: http://localhost:8000/docs
# - MinIO Object Storage Console: http://localhost:9001 (minioadmin / minioadminpassword)
# - Prometheus Metrics: http://localhost:9090
# - Grafana Dashboard: http://localhost:3001 (admin / admin)
```

## Running Python Local Development Stack

```bash
# 1. Seed Database with initial nodes & admin user
python scripts/seed_db.py

# 2. Start FastAPI Aggregator Server
cd backend
uvicorn app.main:app --reload --port 8000

# 3. Start Frontend Dev Server
cd frontend
npm run dev

# 4. Launch Simulated Edge Hospital Nodes
python scripts/run_simulated_hospitals.py
```
