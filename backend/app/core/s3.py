import os
import logging
import boto3
from botocore.exceptions import ClientError
from app.core.config import settings

logger = logging.getLogger(__name__)


class StorageManager:
    def __init__(self):
        self.bucket = settings.MINIO_BUCKET_NAME
        self.local_storage_dir = os.path.abspath("./storage_data")
        os.makedirs(self.local_storage_dir, exist_ok=True)
        self.s3_client = None
        
        try:
            from botocore.config import Config
            protocol = "https" if settings.MINIO_SECURE else "http"
            endpoint = f"{protocol}://{settings.MINIO_ENDPOINT}"
            fast_config = Config(connect_timeout=0.5, read_timeout=0.5, retries={'max_attempts': 0})
            self.s3_client = boto3.client(
                "s3",
                endpoint_url=endpoint,
                aws_access_key_id=settings.MINIO_ACCESS_KEY,
                aws_secret_access_key=settings.MINIO_SECRET_KEY,
                config=fast_config,
            )
            # Check/create bucket
            try:
                self.s3_client.head_bucket(Bucket=self.bucket)
            except ClientError:
                self.s3_client.create_bucket(Bucket=self.bucket)
            logger.info("MinIO/S3 storage initialized successfully.")
        except Exception as e:
            logger.warning(f"S3/MinIO connection failed: {e}. Using local storage directory fallback at {self.local_storage_dir}.")
            self.s3_client = None

    def upload_bytes(self, key: str, data: bytes) -> str:
        if self.s3_client:
            try:
                self.s3_client.put_object(Bucket=self.bucket, Key=key, Body=data)
                return f"s3://{self.bucket}/{key}"
            except Exception as e:
                logger.error(f"S3 upload error: {e}")
        
        # Fallback to filesystem
        filepath = os.path.join(self.local_storage_dir, key.replace("/", "_"))
        with open(filepath, "wb") as f:
            f.write(data)
        return f"file://{filepath}"

    def download_bytes(self, storage_path: str) -> bytes:
        if storage_path.startswith("s3://") and self.s3_client:
            parts = storage_path.replace("s3://", "").split("/", 1)
            bucket, key = parts[0], parts[1]
            response = self.s3_client.get_object(Bucket=bucket, Key=key)
            return response["Body"].read()
        
        # Fallback local file
        clean_path = storage_path.replace("file://", "")
        if os.path.exists(clean_path):
            with open(clean_path, "rb") as f:
                return f.read()
        
        # Check in local storage dir by key basename
        basename = os.path.basename(storage_path)
        alt_path = os.path.join(self.local_storage_dir, basename)
        if os.path.exists(alt_path):
            with open(alt_path, "rb") as f:
                return f.read()
                
        raise FileNotFoundError(f"Storage asset not found at {storage_path}")


storage_manager = StorageManager()
