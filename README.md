# Cross-Hospital Diagnosis Model 🏥⚡

An enterprise-ready, production-grade Federated Learning (FL) healthcare AI platform designed for hospital consortiums to collaboratively train diagnostic models without sharing sensitive patient data (HIPAA & GDPR compliant).

---

## 🌟 Key Features & Capabilities

- **Zero Data-Exposure Federated Learning**: Patient diagnostic EHR records & images stay 100% on-premise inside hospital edge nodes.
- **FedAvg Aggregation**: Central weighted parameter aggregation engine supporting custom PyTorch models & Flower (`flwr`) client/server strategies.
- **Differential Privacy (DP-SGD)**: Local gradient norm clipping ($\ell_2$-bound $C=1.0$) and Gaussian noise injection to prevent model inversion attacks.
- **Clean Architecture & Design Patterns**: FastAPI, SQLAlchemy 2.0 async ORM, Pydantic v2, PostgreSQL, Redis Pub/Sub, and MinIO S3 versioned model weight registry.
- **Enterprise React Portal**: High-impact medical slate dark theme dashboard featuring real-time training telemetry, convergence curves (Chart.js), hospital node management, model registry weight downloads, and HIPAA audit trails.
- **Production Infrastructure**: Complete Docker Compose setup, Kubernetes manifests, Prometheus/Grafana monitoring, and GitHub Actions CI/CD pipeline.

---

## 🏗️ Repository Layout

```
Cross-Hospital Diagnosis Model/
├── backend/                  # FastAPI Aggregator, SQLAlchemy Models, Repositories & Services
│   ├── app/
│   │   ├── api/v1/          # REST & WebSocket Endpoints
│   │   ├── core/            # Config, Security, DB, Redis, S3 Manager
│   │   ├── models/          # PostgreSQL SQLAlchemy ORM Models
│   │   ├── schemas/         # Pydantic Schemas
│   │   ├── repositories/    # Clean Architecture Data Access Layer
│   │   ├── services/        # Business Logic & Aggregation Service
│   │   └── federated/       # FedAvg, Differential Privacy & Flower Adapter
│   ├── tests/               # PyTest Suite (FedAvg, DP, Security)
│   └── Dockerfile
├── hospital_node/            # On-Premise Edge Hospital Agent & Local PyTorch Trainer
│   ├── client/              # Diagnostic Dataset Loader, Local Trainer & DP Engine
│   ├── config.py
│   └── main.py
├── frontend/                 # Vite + React + TypeScript + Tailwind Enterprise Dashboard
│   ├── src/
│   │   ├── components/      # Glassmorphic StatCards, Charts, Modals
│   │   ├── pages/           # Dashboard, Hospitals, Rounds, Models, Audit, Reports
│   │   ├── api/             # Axios API Client
│   │   └── types/           # TypeScript Types & Interfaces
├── docker/                   # Docker Compose, Prometheus & Grafana Configuration
├── kubernetes/               # K8s Deployments, Services, StatefulSets & Ingress
├── docs/                     # Architecture, API Docs, Schema & Security Specs
├── scripts/                  # Seed Script & Simulated Hospital Runner
└── README.md
```

---

## 🚀 Quick Start (Local Setup)

### 1. Seed Database & Run FastAPI Aggregator
```bash
# Seed initial hospitals & admin user
python scripts/seed_db.py

# Start Backend Server
cd backend
uvicorn app.main:app --reload --port 8000
```
- Interactive API Docs: `http://localhost:8000/docs`

### 2. Run React Dashboard
```bash
cd frontend
npm install
npm run dev
```
- Dashboard URL: `http://localhost:5173`

### 3. Launch Simulated Edge Hospital Nodes
```bash
python scripts/run_simulated_hospitals.py
```

---

## 🧪 Testing Suite

Run PyTest unit & integration tests:
```bash
pytest backend/tests -v
```

---

## 🔒 Differential Privacy Guarantee

$$\tilde{\theta}_{global} = \sum_{k=1}^K \frac{n_k}{N} \left( \text{Clip}_C(\theta_k) + \mathcal{N}(0, \sigma^2 C^2 \mathbf{I}) \right)$$

- **Clip Norm ($C$)**: `1.0`
- **Noise Multiplier ($\sigma$)**: `0.05`
- **Privacy Budget**: $(\epsilon, \delta)$ with $\delta = 10^{-5}$
