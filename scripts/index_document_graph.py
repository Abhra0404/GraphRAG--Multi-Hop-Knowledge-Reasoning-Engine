import sys
from pathlib import Path

from extraction.entities import extract_entities
from extraction.relations import extract_relations
from graph.repository import GraphRepository
from ingestion.cleaner import clean_text
from ingestion.chunker import TextChunker
from ingestion.loader import loader

DATASET = "swish_paper"

def main():
    if len(sys.argv) not in (2, 4):
        print(
            "Usage: python -m scripts.index_document_graph "
            "<file> [--start-chunk N]"
        )
        raise SystemExit(1)

    file_path = Path(sys.argv[1])

    if not file_path.exists():
        print(f"File not found: {file_path}")
        raise SystemExit(1)

    start_chunk = 1

    if len(sys.argv) == 4:
        if sys.argv[2] != "--start-chunk":
            print("Unknown argument:", sys.argv[2])
            raise SystemExit(1)

        try:
            start_chunk = int(sys.argv[3])
        except ValueError:
            print("Start chunk must be an integer.")
            raise SystemExit(1)

    text = clean_text(loader.load(str(file_path)))

    chunker = TextChunker(
        chunk_size=1000,
        overlap=150,
    )

    chunks = chunker.split(text)
    repository = GraphRepository()

    total_entities = 0
    total_relations = 0
    failed_chunks = []

    print(f"Processing chunks {start_chunk}-{len(chunks)}...")

    for chunk in chunks:
        chunk_number = chunk.chunk_index + 1

        if chunk_number < start_chunk:
            continue

        print(f"Chunk {chunk_number}/{len(chunks)}")

        try:
            entities = extract_entities(chunk.content)

            for entity in entities:
                repository.upsert_entity(
                    name=entity["name"],
                    entity_type=entity["type"],
                    dataset=DATASET,
                    source_document=file_path.name,
                    source_chunk=chunk.chunk_index,
                )

            total_entities += len(entities)

            relations = extract_relations(
                chunk.content,
                entities,
            )

            for relation in relations:
                repository.upsert_relation(
                    source=relation["source"],
                    relation=relation["relation"],
                    target=relation["target"],
                    dataset=DATASET,
                    source_document=file_path.name,
                    source_chunk=chunk.chunk_index,
                )

            total_relations += len(relations)

        except Exception as exc:
            failed_chunks.append(chunk_number)

            print(
                f"Warning: Chunk {chunk_number} failed: "
                f"{type(exc).__name__}: {exc}"
            )
            print("Skipping chunk and continuing...")

    print()
    print("Graph indexing complete.")
    print(f"Entities:       {total_entities}")
    print(f"Relations:      {total_relations}")
    print(f"Failed chunks:  {failed_chunks}")
    print(f"Source:         {file_path.name}")


if __name__ == "__main__":
    main()