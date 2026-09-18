import logging

from fastapi import FastAPI
from qdrant_client import QdrantClient
from sqlalchemy import text

from apps.api.routes.query import router as query_router
from core.config import settings
from core.database import engine
from core.logging import setup_logging
from graph.client import neo4j_client


setup_logging()

logger = logging.getLogger(__name__)

app = FastAPI(
    title="GraphRAG API",
    description=(
        "Knowledge Graph + Vector Retrieval system "
        "for multi-hop reasoning over documents."
    ),
    version="1.0.0",
)


def verify_postgres_connection() -> bool:
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return True
    except Exception:
        return False


def verify_qdrant_connection() -> bool:
    try:
        client = QdrantClient(url=settings.qdrant_url)
        client.get_collections()
        return True
    except Exception:
        return False


@app.get("/health")
def health():
    return {
        "status": "ok",
        "services": {
            "postgres": verify_postgres_connection(),
            "neo4j": neo4j_client.verify_connection(),
            "qdrant": verify_qdrant_connection(),
        },
    }


app.include_router(query_router)