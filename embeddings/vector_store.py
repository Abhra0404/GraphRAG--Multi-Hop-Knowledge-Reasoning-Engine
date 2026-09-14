from qdrant_client import QdrantClient

from core.config import settings


qdrant_client = QdrantClient(
    url=settings.qdrant_url,
)


def verify_connection() -> bool:
    try:
        qdrant_client.get_collections()
        return True
    except Exception:
        return False