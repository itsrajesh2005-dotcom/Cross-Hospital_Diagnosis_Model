# PostgreSQL Database Schema Specification

The database utilizes PostgreSQL with SQLAlchemy 2.0 async ORM and UUID primary keys.

## Core Tables

### 1. `hospitals`
- `id` (UUID, PK)
- `name` (VARCHAR)
- `code` (VARCHAR, Unique)
- `api_key_hash` (VARCHAR)
- `endpoint_url` (VARCHAR)
- `dataset_sample_count` (INTEGER)
- `status` (VARCHAR) - `ACTIVE`, `OFFLINE`, `TRAINING`
- `last_heartbeat` (TIMESTAMP)
- `location` (VARCHAR)
- `is_verified` (BOOLEAN)

### 2. `users`
- `id` (UUID, PK)
- `hospital_id` (UUID, FK -> hospitals.id)
- `email` (VARCHAR, Unique)
- `password_hash` (VARCHAR)
- `full_name` (VARCHAR)
- `role` (VARCHAR) - `SYSTEM_ADMIN`, `HOSPITAL_ADMIN`, `AUDITOR`
- `is_active` (BOOLEAN)

### 3. `training_rounds`
- `id` (UUID, PK)
- `round_number` (INTEGER, Unique)
- `status` (VARCHAR) - `IDLE`, `SELECTING`, `TRAINING`, `AGGREGATING`, `COMPLETED`
- `target_accuracy` (FLOAT)
- `min_clients` (INTEGER)
- `participating_clients_count` (INTEGER)
- `current_accuracy` (FLOAT)
- `current_loss` (FLOAT)

### 4. `global_models`
- `id` (UUID, PK)
- `round_id` (UUID, FK -> training_rounds.id)
- `version` (VARCHAR, Unique)
- `s3_storage_path` (TEXT)
- `accuracy` (FLOAT)
- `loss` (FLOAT)
- `f1_score` (FLOAT)

### 5. `local_models`
- `id` (UUID, PK)
- `round_id` (UUID, FK -> training_rounds.id)
- `hospital_id` (UUID, FK -> hospitals.id)
- `s3_storage_path` (TEXT)
- `sample_count` (INTEGER)
- `local_loss` (FLOAT)
- `local_accuracy` (FLOAT)
- `dp_epsilon` (FLOAT)
- `dp_delta` (FLOAT)

### 6. `audit_logs`
- `id` (UUID, PK)
- `user_id` (UUID, FK -> users.id)
- `action` (VARCHAR)
- `resource_type` (VARCHAR)
- `ip_address` (VARCHAR)
- `details` (JSON)
