from extraction.entities import extract_entities
from extraction.relations import extract_relations


TEXT = """
Albert Einstein developed the theory of relativity.
He was born in Germany and later worked in Switzerland.
"""


def main():
    entities = extract_entities(TEXT)

    print("\n--- Entities ---")
    for entity in entities:
        print(entity)

    relations = extract_relations(TEXT, entities)

    print("\n--- Relations ---")
    for relation in relations:
        print(relation)


if __name__ == "__main__":
    main()