import logging
import redis.asyncio as redis
from app.core.config import settings

logger = logging.getLogger(__name__)

redis_client: redis.Redis | None = None


async def get_redis_client() -> redis.Redis | None:
    global redis_client
    if redis_client is None:
        try:
            redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)
            await redis_client.ping()
            logger.info("Connected to Redis successfully.")
        except Exception as e:
            logger.warning(f"Could not connect to Redis server ({e}). Falling back to memory state.")
            redis_client = None
    return redis_client
