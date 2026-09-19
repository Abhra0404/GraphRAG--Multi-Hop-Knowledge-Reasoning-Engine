from reasoning.chain import build_reasoning_chains
from reasoning.path_ranker import rank_paths
from reasoning.reasoner import build_valid_reasoning_chains
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
        limit=10,
    )

    chains = build_reasoning_chains(ranked_paths)

    valid_chains = build_valid_reasoning_chains(
        chains,
        query_entities,
    )

    print("\n--- Valid Reasoning Chains ---")

    for chain in valid_chains:
        print(chain)


if __name__ == "__main__":
    main()