from extraction.entities import extract_entities
from extraction.relations import extract_relations
from graph.repository import graph_repository


TEXT = """
Albert Einstein developed the theory of relativity.
He was born in Germany and later worked in Switzerland.
"""


def main():
    entities = extract_entities(TEXT)

    print("\n--- Entities ---")
    for entity in entities:
        print(entity)
        graph_repository.upsert_entity(
            name=entity["name"],
            entity_type=entity["type"],
        )

    relations = extract_relations(TEXT, entities)

    print("\n--- Relations ---")
    for relation in relations:
        print(relation)
        graph_repository.upsert_relation(
            source=relation["source"],
            relation=relation["relation"],
            target=relation["target"],
        )

    print("\nGraph construction complete.")


if __name__ == "__main__":
    main()