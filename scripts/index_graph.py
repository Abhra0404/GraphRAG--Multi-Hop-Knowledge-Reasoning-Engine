from pathlib import Path

from extraction.entities import extract_entities
from extraction.relations import extract_relations
from graph.repository import graph_repository
from ingestion.chunker import TextChunker
from ingestion.cleaner import clean_text
from ingestion.loader import loader


def main():
    file_path = Path("data/multihop.txt")

    text = loader.load(str(file_path))
    text = clean_text(text)

    chunker = TextChunker(
        chunk_size=1000,
        overlap=150,
    )

    chunks = chunker.split(text)

    total_entities = 0
    total_relations = 0

    for chunk in chunks:
        entities = extract_entities(chunk.content)

        for entity in entities:
            graph_repository.upsert_entity(
                name=entity["name"],
                entity_type=entity["type"],
            )

        relations = extract_relations(
            chunk.content,
            entities,
        )

        for relation in relations:
            graph_repository.upsert_relation(
                source=relation["source"],
                relation=relation["relation"],
                target=relation["target"],
                source_document=file_path.name,
                source_chunk=chunk.chunk_index,
            )

        total_entities += len(entities)
        total_relations += len(relations)

    print(f"Processed {len(chunks)} chunks.")
    print(f"Extracted {total_entities} entities.")
    print(f"Extracted {total_relations} relations.")
    print("Graph indexing complete.")


if __name__ == "__main__":
    main()