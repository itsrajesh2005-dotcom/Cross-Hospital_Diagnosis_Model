# Cross-Hospital Diagnosis Model - Platform Architecture

## Executive Architecture Summary

The **Cross-Hospital Diagnosis Model** platform is designed to allow multiple healthcare providers (e.g., St. Jude, Mayo Clinic, Johns Hopkins) to collaboratively train diagnostic AI models without exposing patient data.

### Core Architectural Principles
1. **Data Sovereignty & Zero-Knowledge**: Patient Electronic Health Records (EHR) and diagnostic images remain strictly on-premise inside hospital edge nodes.
2. **Federated Averaging (FedAvg)**: The central aggregator computes weighted parameter updates based on local dataset sizes:
   $$\theta_{global} = \sum_{k=1}^K \frac{n_k}{N} \theta_k$$
3. **Differential Privacy (DP-SGD)**: Local updates apply $\ell_2$-norm gradient clipping and Gaussian noise injection to prevent model inversion and membership inference attacks.
4. **Clean Architecture**: Decoupled repository, service, controller, and infrastructure layers built on Python 3.12, FastAPI, SQLAlchemy 2.0, PostgreSQL, Redis, MinIO S3, and React TypeScript.

---

## High-Level Topology

```
                  +--------------------------------------------------+
                  |         Enterprise React Dashboard               |
                  +------------------------+-------------------------+
                                           |
                                           v
                  +--------------------------------------------------+
                  |            FastAPI Aggregator Gateway            |
                  +----+-------------------+-------------------+-----+
                       |                   |                   |
                       v                   v                   v
              +-----------------+ +-----------------+ +-----------------+
              |   PostgreSQL    | |   Redis State   | |  MinIO / S3     |
              | (Metadata & DB) | |  (Pub/Sub & WS) | | (Model Weights)|
              +-----------------+ +-----------------+ +-----------------+
                                           ^
                                           | (Encrypted Model Updates & DP Noise)
         +---------------------------------+---------------------------------+
         |                                 |                                 |
         v                                 v                                 v
+------------------+             +------------------+             +------------------+
| Hospital Node A  |             | Hospital Node B  |             | Hospital Node C  |
|  (Local Datasets)|             |  (Local Datasets)|             |  (Local Datasets)|
+------------------+             +------------------+             +------------------+
```
