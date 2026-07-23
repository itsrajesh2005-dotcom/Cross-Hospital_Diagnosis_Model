import os


class HospitalNodeConfig:
    HOSPITAL_NAME: str = os.getenv("HOSPITAL_NAME", "St. Jude Children's Research Hospital")
    HOSPITAL_CODE: str = os.getenv("HOSPITAL_CODE", "HOSP_STJUDE")
    AGGREGATOR_URL: str = os.getenv("AGGREGATOR_URL", "http://localhost:8000/api/v1")
    DATASET_SIZE: int = int(os.getenv("DATASET_SIZE", "1200"))
    LOCAL_EPOCHS: int = int(os.getenv("LOCAL_EPOCHS", "3"))
    BATCH_SIZE: int = int(os.getenv("BATCH_SIZE", "32"))
    LEARNING_RATE: float = float(os.getenv("LEARNING_RATE", "0.001"))
    
    # Differential Privacy Settings
    ENABLE_DP: bool = True
    CLIP_NORM: float = 1.0
    NOISE_MULTIPLIER: float = 0.05
    DP_DELTA: float = 1e-5


node_config = HospitalNodeConfig()
