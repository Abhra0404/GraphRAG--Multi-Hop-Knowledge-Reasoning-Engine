from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    PointStruct,
    VectorParams,
)

from core.config import settings
from embeddings.embedder import embedding_dimension


COLLECTION_NAME = "document_chunks"


qdrant_client = QdrantClient(
    url=settings.qdrant_url,
)


def create_collection() -> None:
    collections = qdrant_client.get_collections()

    existing = {
        collection.name
        for collection in collections.collections
    }

    if COLLECTION_NAME in existing:
        return

    qdrant_client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(
            size=embedding_dimension(),
            distance=Distance.COSINE,
        ),
    )


def upsert_chunks(
    points: list[PointStruct],
) -> None:
    if not points:
        return

    qdrant_client.upsert(
        collection_name=COLLECTION_NAME,
        points=points,
    )


def search(
    query_vector: list[float],
    limit: int = 5,
):
    return qdrant_client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=limit,
    ).points