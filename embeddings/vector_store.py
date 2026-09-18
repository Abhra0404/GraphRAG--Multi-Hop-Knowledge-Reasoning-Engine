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


def create_collection(
    collection_name: str = COLLECTION_NAME,
) -> None:
    collections = qdrant_client.get_collections()

    existing = {
        collection.name
        for collection in collections.collections
    }

    if collection_name in existing:
        return

    qdrant_client.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(
            size=embedding_dimension(),
            distance=Distance.COSINE,
        ),
    )


def upsert_chunks(
    points: list[PointStruct],
    collection_name: str = COLLECTION_NAME,
) -> None:
    if not points:
        return

    qdrant_client.upsert(
        collection_name=collection_name,
        points=points,
    )


def search(
    query_vector: list[float],
    limit: int = 5,
    collection_name: str = COLLECTION_NAME,
):
    return qdrant_client.query_points(
        collection_name=collection_name,
        query=query_vector,
        limit=limit,
    ).points