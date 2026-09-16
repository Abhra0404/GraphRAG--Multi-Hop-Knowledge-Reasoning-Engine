import json
from pathlib import Path


RESULTS_PATH = Path("evaluation/results.json")


def save_results(results: list[dict]) -> None:
    RESULTS_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with RESULTS_PATH.open("w", encoding="utf-8") as file:
        json.dump(
            results,
            file,
            indent=2,
            ensure_ascii=False,
        )


def print_summary(results: list[dict]) -> None:
    total = len(results)

    if total == 0:
        return

    answer_similarity = sum(
        result["answer_similarity"]
        for result in results
    ) / total

    entity_recall = sum(
        result["entity_recall"]
        for result in results
    ) / total

    relationship_recall = sum(
        result["relationship_recall"]
        for result in results
    ) / total

    reasoning_recall = sum(
        result["reasoning_recall"]
        for result in results
    ) / total

    citation_presence = sum(
        result["citation_correct"]
        for result in results
    ) / total

    print("\n=== GraphRAG Evaluation ===")
    print(f"\nCases: {total}")

    print(
        f"\nAnswer Similarity       "
        f"{answer_similarity:.2f}"
    )

    print(
        f"Entity Recall           "
        f"{entity_recall:.2f}"
    )

    print(
        f"Relationship Recall     "
        f"{relationship_recall:.2f}"
    )

    print(
        f"Reasoning Recall        "
        f"{reasoning_recall:.2f}"
    )

    print(
        f"Citation Presence       "
        f"{citation_presence:.2f}"
    )

    print(
        f"\nResults saved to        "
        f"{RESULTS_PATH}"
    )