from embeddings.embedder import (
    embed_texts,
    embedding_dimension,
)


def test_embedding_dimension():
    dimension = embedding_dimension()

    assert dimension == 384


def test_embed_texts():
    texts = [
        "Knowledge graphs represent relationships.",
        "Vector databases store embeddings.",
    ]

    embeddings = embed_texts(texts)

    assert len(embeddings) == 2
    assert len(embeddings[0]) == 384
    assert len(embeddings[1]) == 384