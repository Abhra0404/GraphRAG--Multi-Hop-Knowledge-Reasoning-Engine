from pathlib import Path
import uuid
from qdrant_client.models import PointStruct

from embeddings.embedder import embed_texts
from embeddings.vector_store import create_collection, upsert_chunks
from ingestion.chunker import TextChunker
from ingestion.cleaner import clean_text
from ingestion.loader import loader


def main():
    file_path = Path("data/sample.txt")

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

    create_collection()

    points = []

    for chunk, embedding in zip(chunks, embeddings):
        points.append(
            PointStruct(
                id=str(
                    uuid.uuid5(
                        uuid.NAMESPACE_URL,
                        f"{file_path.name}:{chunk.chunk_index}",
                    )
                ),
                vector=embedding,
                payload={
                    "content": chunk.content,
                    "chunk_index": chunk.chunk_index,
                    "source": file_path.name,
                },
            )
        )

    upsert_chunks(points)

    print(f"Indexed {len(points)} chunks.")


if __name__ == "__main__":
    main()