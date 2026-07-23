# REST & WebSocket API Documentation

Base URL: `http://localhost:8000/api/v1`

## Authentication APIs
- `POST /api/v1/auth/login`: Authenticate user and return JWT bearer token.
- `POST /api/v1/auth/register`: Register new consortium administrator or researcher.

## Hospital Management APIs
- `GET /api/v1/hospitals`: List all registered hospital edge nodes.
- `GET /api/v1/hospitals/{id}`: Fetch detailed hospital metadata by UUID.
- `POST /api/v1/hospitals/register-node`: Register a new hospital edge node and issue credentials.
- `POST /api/v1/hospitals/{code}/heartbeat`: Edge node heartbeat ping.

## Federated Rounds APIs
- `GET /api/v1/rounds`: List all historical and active federated training rounds.
- `POST /api/v1/rounds/start`: Trigger a new federated training round across eligible nodes.
- `POST /api/v1/rounds/{id}/submit-update`: Submit local PyTorch model updates with DP noise.

## Model Registry & Storage APIs
- `GET /api/v1/models/global`: List all global aggregated model versions.
- `GET /api/v1/models/global/latest`: Get latest versioned global PyTorch model metadata.
- `GET /api/v1/models/{id}/download`: Download compiled global PyTorch binary weights (`.pt`).

## Dashboard, Audit & Telemetry APIs
- `GET /api/v1/dashboard/summary`: High-level consortium statistics and live activity.
- `GET /api/v1/metrics/training`: Convergence telemetry (Accuracy & Loss curves).
- `GET /api/v1/audit/logs`: HIPAA security audit event trail.
- `GET /api/v1/reports/summary`: Consortium executive summary report data.
- `WS /api/v1/ws/rounds`: Real-time WebSocket telemetry stream.
