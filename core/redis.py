import redis

from core.config import settings


redis_client = redis.Redis.from_url(
    settings.redis_url,
    decode_responses=True,
)


def verify_connection() -> bool:
    try:
        return redis_client.ping()
    except Exception:
        return False