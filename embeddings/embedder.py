from functools import lru_cache

from sentence_transformers import SentenceTransformer

from core.config import settings


@lru_cache
def get_embedder() -> SentenceTransformer:
    return SentenceTransformer(settings.embedding_model)


def embed_texts(texts: list[str]) -> list[list[float]]:
    if not texts:
        return []

    model = get_embedder()

    embeddings = model.encode(
        texts,
        normalize_embeddings=True,
        show_progress_bar=False,
    )

    return embeddings.tolist()


def embedding_dimension() -> int:
    model = get_embedder()
    return model.get_sentence_embedding_dimension()