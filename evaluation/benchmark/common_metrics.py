import json
from pathlib import Path

from embeddings.embedder import embed_texts
from embeddings.vector_store import search
from graph.client import neo4j_client
from reasoning.path_ranker import rank_paths
from retrieval.graph import retrieve_graph

from evaluation.benchmark.corpus import RELATIONS


DATASET_PATH = Path(
    "evaluation/benchmark/data/benchmark_dataset.json"
)

COLLECTION_NAME = "benchmark_chunks"


def get_benchmark_entities() -> list[str]:
    query = """
    MATCH (e:Entity {dataset: "benchmark"})
    RETURN DISTINCT e.name AS name
    """

    with neo4j_client.driver.session() as session:
        return [
            record["name"]
            for record in session.run(query)
        ]


def detect_question_entities(
    question: str,
    entity_names: list[str],
) -> list[str]:
    question_lower = question.lower()

    matches = [
        entity
        for entity in entity_names
        if entity.lower() in question_lower
    ]

    return sorted(
        matches,
        key=len,
        reverse=True,
    )


def get_expected_path(case: dict) -> list[tuple[str, str, str]]:
    expected_entities = case["expected_entities"]
    expected_relationships = case["expected_relationships"]

    if not expected_relationships:
        return []

    paths = []

    for start in expected_entities:
        for source, relation, target in RELATIONS:
            if source.lower() != start.lower():
                continue

            if relation.upper() != expected_relationships[0].upper():
                continue

            current_path = [(source, relation, target)]

            for expected_relation in expected_relationships[1:]:
                current_target = current_path[-1][2]

                next_edge = next(
                    (
                        edge
                        for edge in RELATIONS
                        if (
                            edge[0].lower()
                            == current_target.lower()
                            and edge[1].upper()
                            == expected_relation.upper()
                        )
                    ),
                    None,
                )

                if next_edge is None:
                    break

                current_path.append(next_edge)

            if len(current_path) == len(expected_relationships):
                paths.append(current_path)

    return paths


def path_matches_expected(
    path: dict,
    expected_paths: list[list[tuple[str, str, str]]],
) -> bool:
    nodes = path.get("nodes", [])
    relationships = path.get("relationships", [])

    if not expected_paths:
        return False

    actual_edges = [
        (nodes[index], relationships[index], nodes[index + 1])
        for index in range(len(relationships))
    ]

    for expected_path in expected_paths:
        if len(actual_edges) != len(expected_path):
            continue

        if all(
            actual[0].lower() == expected[0].lower()
            and actual[1].upper() == expected[1].upper()
            and actual[2].lower() == expected[2].lower()
            for actual, expected in zip(
                actual_edges,
                expected_path,
            )
        ):
            return True

    return False


def vanilla_fact_recall(case: dict) -> float:
    question = case["question"]
    expected_relationships = case["expected_relationships"]

    if not expected_relationships:
        return 1.0

    query_embedding = embed_texts([question])[0]

    results = search(
        query_vector=query_embedding,
        limit=5,
        collection_name=COLLECTION_NAME,
    )

    text = "\n".join(
        result.payload.get("content", "")
        for result in results
    ).lower()

    hits = sum(
        relationship.lower() in text
        for relationship in expected_relationships
    )

    return hits / len(expected_relationships)


def graphrag_path_recall(
    case: dict,
    entity_names: list[str],
) -> float:
    expected_relationships = case["expected_relationships"]
    required_hops = case["required_hops"]

    if not expected_relationships:
        return 1.0

    detected_entities = detect_question_entities(
        case["question"],
        entity_names,
    )

    paths = []

    for entity in detected_entities:
        paths.extend(
            retrieve_graph(
                entity,
                hops=required_hops,
                dataset="benchmark",
            )
        )

    ranked_paths = rank_paths(
        paths=paths,
        query_entities=detected_entities,
        limit=5,
    )

    expected_paths = get_expected_path(case)

    return (
        1.0
        if any(
            path_matches_expected(
                path,
                expected_paths,
            )
            for path in ranked_paths
        )
        else 0.0
    )


def average(scores: list[float]) -> float:
    return (
        sum(scores) / len(scores)
        if scores
        else 0.0
    )


def main():
    with DATASET_PATH.open(
        encoding="utf-8"
    ) as file:
        dataset = json.load(file)

    entity_names = get_benchmark_entities()

    positive_cases = [
        case
        for case in dataset
        if case["required_hops"] > 0
    ]

    print("\n=== Exact Path Retrieval Benchmark ===\n")
    print(f"Positive Cases: {len(positive_cases)}")

    all_vanilla = []
    all_graphrag = []

    for hops in [1, 2, 3]:
        cases = [
            case
            for case in positive_cases
            if case["required_hops"] == hops
        ]

        vanilla_scores = [
            vanilla_fact_recall(case)
            for case in cases
        ]

        graphrag_scores = [
            graphrag_path_recall(
                case,
                entity_names,
            )
            for case in cases
        ]

        vanilla = average(vanilla_scores)
        graphrag = average(graphrag_scores)

        all_vanilla.extend(vanilla_scores)
        all_graphrag.extend(graphrag_scores)

        print(f"\n{hops}-hop ({len(cases)} cases)")
        print(f"  Vanilla RAG: {vanilla:.2f}")
        print(f"  GraphRAG:    {graphrag:.2f}")
        print(
            f"  Difference:  "
            f"{graphrag - vanilla:+.2f}"
        )

    vanilla = average(all_vanilla)
    graphrag = average(all_graphrag)

    print("\n=== Positive-Case Overall ===")
    print(f"Vanilla RAG: {vanilla:.2f}")
    print(f"GraphRAG:    {graphrag:.2f}")
    print(
        f"Absolute difference: "
        f"{graphrag - vanilla:+.2f}"
    )

    if vanilla > 0:
        print(
            f"Relative improvement: "
            f"{((graphrag - vanilla) / vanilla) * 100:.1f}%"
        )


if __name__ == "__main__":
    main()