import os
from typing import List, Union
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "Cross-Hospital Diagnosis Model"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    # CORS
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:8000",
    ]

    # JWT Security
    SECRET_KEY: str = "SUPER_SECRET_ENTERPRISE_HEALTHCARE_FL_KEY_CHANGE_IN_PROD_998877"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 1 day

    # Database Configuration
    USE_SQLITE: bool = True
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "cross_hospital_fl"
    POSTGRES_PORT: str = "5432"
    SQLALCHEMY_DATABASE_URI: str = ""

    def model_post_init(self, __context):
        if not self.SQLALCHEMY_DATABASE_URI:
            if self.USE_SQLITE:
                self.SQLALCHEMY_DATABASE_URI = "sqlite+aiosqlite:///./sql_app.db"
            else:
                self.SQLALCHEMY_DATABASE_URI = (
                    f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@"
                    f"{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
                )

    # Redis Configuration
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_URL: str = "redis://localhost:6379/0"

    # MinIO / S3 Object Storage
    MINIO_ENDPOINT: str = "localhost:9000"
    MINIO_ACCESS_KEY: str = "minioadmin"
    MINIO_SECRET_KEY: str = "minioadmin"
    MINIO_BUCKET_NAME: str = "fl-model-registry"
    MINIO_SECURE: bool = False

    # Federated Learning Defaults
    DEFAULT_MIN_CLIENTS_PER_ROUND: int = 2
    DEFAULT_TARGET_ACCURACY: float = 0.95
    DP_GRADIENT_CLIP: float = 1.0
    DP_NOISE_MULTIPLIER: float = 0.1
    DP_DELTA: float = 1e-5

    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_file=(
            os.path.abspath(".env"),
            os.path.abspath("backend/.env"),
            os.path.abspath("../.env"),
        ),
        extra="allow"
    )


settings = Settings()
