from sqlalchemy import text

from core.database import engine
from embeddings.vector_store import qdrant_client
from graph.client import neo4j_client


def check_postgres() -> bool:
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        return True
    except Exception:
        return False


def check_neo4j() -> bool:
    return neo4j_client.verify_connection()


def check_qdrant() -> bool:
    try:
        qdrant_client.get_collections()
        return True
    except Exception:
        return False

def check_all_services():
    services = {
        "postgres": check_postgres(),
        "neo4j": check_neo4j(),
        "qdrant": check_qdrant(),
    }

    status = (
        "ok"
        if all(services.values())
        else "degraded"
    )

    return {
        "status": status,
        "services": {
            name: "healthy" if healthy else "unhealthy"
            for name, healthy in services.items()
        },
    }