from evaluation.benchmark.corpus import RELATIONS
from graph.client import neo4j_client


def main():
    query = """
    MERGE (source:Entity {
        name: $source,
        dataset: "benchmark"
    })

    MERGE (target:Entity {
        name: $target,
        dataset: "benchmark"
    })

    MERGE (source)-[r:RELATED {
        type: $relation,
        dataset: "benchmark"
    }]->(target)

    SET
        r.source_document = "benchmark_corpus.txt",
        r.source_chunk = 0
    """

    with neo4j_client.driver.session() as session:
        for source, relation, target in RELATIONS:
            session.run(
                query,
                source=source,
                relation=relation,
                target=target,
            )

    print(
        f"Indexed {len(RELATIONS)} benchmark relationships."
    )


if __name__ == "__main__":
    main()
    