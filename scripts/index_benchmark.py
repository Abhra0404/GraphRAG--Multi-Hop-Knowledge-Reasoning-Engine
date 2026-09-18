from pathlib import Path
import uuid

from qdrant_client.models import PointStruct

from embeddings.embedder import embed_texts
from embeddings.vector_store import (
    create_collection,
    upsert_chunks,
)
from ingestion.chunker import TextChunker
from ingestion.cleaner import clean_text
from ingestion.loader import loader


COLLECTION_NAME = "benchmark_chunks"


def main():
    file_path = Path(
        "evaluation/benchmark/data/benchmark_corpus.txt"
    )

    text = loader.load(str(file_path))
    text = clean_text(text)

    chunker = TextChunker(
        chunk_size=1000,
        overlap=150,
    )

    chunks = chunker.split(text)

    embeddings = embed_texts(
        [chunk.content for chunk in chunks]
    )

    create_collection(COLLECTION_NAME)

    points = []

    for chunk, embedding in zip(chunks, embeddings):
        points.append(
            PointStruct(
                id=str(
                    uuid.uuid5(
                        uuid.NAMESPACE_URL,
                        f"benchmark:{file_path.name}:{chunk.chunk_index}",
                    )
                ),
                vector=embedding,
                payload={
                    "content": chunk.content,
                    "chunk_index": chunk.chunk_index,
                    "source": file_path.name,
                    "dataset": "benchmark",
                },
            )
        )

    upsert_chunks(
        points,
        collection_name=COLLECTION_NAME,
    )

    print(
        f"Indexed {len(points)} benchmark chunks."
    )


if __name__ == "__main__":
    main()