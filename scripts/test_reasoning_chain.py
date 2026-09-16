from reasoning.chain import build_reasoning_chains
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

    ranked_paths = rank_paths(
        paths,
        query_entities,
        limit=5,
    )

    chains = build_reasoning_chains(ranked_paths)

    print("\n--- Reasoning Chains ---")

    for chain in chains:
        print(chain)


if __name__ == "__main__":
    main()