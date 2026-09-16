from reasoning.path_ranker import rank_paths
from retrieval.graph import retrieve_graph


def main():
    query_entities = [
        "Einstein",
        "spacetime",
    ]

    paths = []

    for entity in query_entities:
        paths.extend(
            retrieve_graph(
                entity,
                hops=2,
            )
        )

    ranked = rank_paths(
        paths,
        query_entities,
        limit=5,
    )

    print("\n--- Ranked Paths ---")

    for path in ranked:
        print(
            {
                "score": path["score"],
                "nodes": path["nodes"],
                "relationships": path["relationships"],
            }
        )


if __name__ == "__main__":
    main()