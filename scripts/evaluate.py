import re
from evaluation.dataset import EVALUATION_DATASET
from evaluation.metrics import (
    answer_contains_expected,
    entity_recall,
    reasoning_chain_recall,
    relationship_recall,
    semantic_answer_similarity,
)
from reasoning.pipeline import answer_query
from evaluation.report import (
    save_results,
    print_summary,
)


def evaluate_case(case: dict) -> dict:
    result = answer_query(case["question"])

    answer = result["answer"]
    chains = result["reasoning_chains"]

    detected_entities = result["entities"]

    detected_relationships = [
        step.relationship
        for chain in chains
        for step in chain.steps
    ]

    citation_type = case["expected_citation_type"]

    if citation_type == "chain":
        citation_correct = bool(
            re.search(
                r"\[Chain\s+\d+\]",
                answer.replace("\u202f", " "),
            )
        )

    elif citation_type == "text":
        citation_correct = bool(
            re.search(
                r"\[Text\s+\d+\]",
                answer.replace("\u202f", " "),
            )
        )

    else:
        citation_correct = True

    return {
        "id": case["id"],
        "question": case["question"],
        "answer_similarity": semantic_answer_similarity(
            answer,
            case["expected_answer"],
        ),
        "entity_recall": entity_recall(
            detected_entities,
            case["expected_entities"],
        ),
        "relationship_recall": relationship_recall(
            detected_relationships,
            case["expected_relationships"],
        ),
        "reasoning_recall": reasoning_chain_recall(
            chains,
            case["expected_relationships"],
            case["required_hops"],
        ),
        "citation_correct": citation_correct,
    }


def main():
    results = []

    for case in EVALUATION_DATASET:
        print(f"\nEvaluating: {case['id']}")

        result = evaluate_case(case)
        results.append(result)

        print(
            f"Answer similarity: "
            f"{result['answer_similarity']:.2f}"
        )
        print(f"Entity recall: {result['entity_recall']:.2f}")
        print(
            f"Relationship recall: "
            f"{result['relationship_recall']:.2f}"
        )
        print(
            f"Reasoning recall: "
            f"{result['reasoning_recall']:.2f}"
        )
        print(
            f"Citation correct: "
            f"{result['citation_correct']}"
        )

    total = len(results)

    save_results(results)
    print_summary(results)


if __name__ == "__main__":
    main()