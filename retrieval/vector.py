from embeddings.embedder import embed_texts
from embeddings.vector_store import search


def retrieve(
    query: str,
    limit: int = 5,
    collection_name: str = "document_chunks",
):
    query_embedding = embed_texts([query])[0]

    return search(
        query_vector=query_embedding,
        limit=limit,
        collection_name=collection_name,
    )