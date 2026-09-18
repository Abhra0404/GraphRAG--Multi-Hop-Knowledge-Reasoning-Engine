import json
from pathlib import Path

from evaluation.benchmark.corpus import RELATIONS


OUTPUT_PATH = Path(
    "evaluation/benchmark/data/benchmark_dataset.json"
)


def build_single_hop_questions() -> list[dict]:
    questions = []

    for index, (source, relation, target) in enumerate(RELATIONS):
        relation_text = relation.lower().replace("_", " ")

        questions.append(
            {
                "id": f"single_hop_{index + 1:03d}",
                "question": f"What {relation_text} {source}?",
                "expected_entities": [source],
                "expected_relationships": [relation],
                "expected_answer": (
                    f"{source} {relation_text} {target}."
                ),
                "required_hops": 1,
                "expected_citation_type": "chain",
            }
        )

    return questions


def build_two_hop_questions() -> list[dict]:
    questions = []

    for index, first in enumerate(RELATIONS):
        source, relation_1, intermediate = first

        for relation_2_item in RELATIONS:
            intermediate_2, relation_2, target = relation_2_item

            if intermediate.lower() != intermediate_2.lower():
                continue

            questions.append(
                {
                    "id": f"two_hop_{index + 1:03d}_{len(questions) + 1:03d}",
                    "question": (
                        f"How is {source} connected to {target}?"
                    ),
                    "expected_entities": [
                        source,
                        target,
                    ],
                    "expected_relationships": [
                        relation_1,
                        relation_2,
                    ],
                    "expected_answer": (
                        f"{source} {relation_1.lower().replace('_', ' ')} "
                        f"{intermediate}, which "
                        f"{relation_2.lower().replace('_', ' ')} "
                        f"{target}."
                    ),
                    "required_hops": 2,
                    "expected_citation_type": "chain",
                }
            )

    return questions


def build_three_hop_questions() -> list[dict]:
    questions = []

    for source, relation_1, intermediate_1 in RELATIONS:
        for (
            intermediate_2,
            relation_2,
            intermediate_3,
        ) in RELATIONS:
            if intermediate_1.lower() != intermediate_2.lower():
                continue

            for (
                intermediate_4,
                relation_3,
                target,
            ) in RELATIONS:
                if intermediate_3.lower() != intermediate_4.lower():
                    continue

                questions.append(
                    {
                        "id": f"three_hop_{len(questions) + 1:03d}",
                        "question": (
                            f"What is the connection between "
                            f"{source} and {target}?"
                        ),
                        "expected_entities": [
                            source,
                            target,
                        ],
                        "expected_relationships": [
                            relation_1,
                            relation_2,
                            relation_3,
                        ],
                        "expected_answer": (
                            f"{source} "
                            f"{relation_1.lower().replace('_', ' ')} "
                            f"{intermediate_1}, which "
                            f"{relation_2.lower().replace('_', ' ')} "
                            f"{intermediate_3}, which "
                            f"{relation_3.lower().replace('_', ' ')} "
                            f"{target}."
                        ),
                        "required_hops": 3,
                        "expected_citation_type": "chain",
                    }
                )

    return questions


def build_dataset() -> list[dict]:
    single_hop = build_single_hop_questions()
    two_hop = build_two_hop_questions()
    three_hop = build_three_hop_questions()
    negative = build_negative_questions()

    return (
        single_hop
        + two_hop
        + three_hop
        + negative
    )


def save_dataset(dataset: list[dict]) -> None:
    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    OUTPUT_PATH.write_text(
        json.dumps(
            dataset,
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

def build_negative_questions() -> list[dict]:
    return [
        {
            "id": "negative_001",
            "question": "Who discovered quantum mechanics?",
            "expected_entities": [],
            "expected_relationships": [],
            "expected_answer": None,
            "required_hops": 0,
            "expected_citation_type": "none",
        },
        {
            "id": "negative_002",
            "question": "What did Leonardo da Vinci develop?",
            "expected_entities": [],
            "expected_relationships": [],
            "expected_answer": None,
            "required_hops": 0,
            "expected_citation_type": "none",
        },
        {
            "id": "negative_003",
            "question": "Who invented the telephone?",
            "expected_entities": [],
            "expected_relationships": [],
            "expected_answer": None,
            "required_hops": 0,
            "expected_citation_type": "none",
        },
        {
            "id": "negative_004",
            "question": "What is the relationship between quantum mechanics and Tesla?",
            "expected_entities": [],
            "expected_relationships": [],
            "expected_answer": None,
            "required_hops": 0,
            "expected_citation_type": "none",
        },
        {
            "id": "negative_005",
            "question": "What did Galileo discover?",
            "expected_entities": [],
            "expected_relationships": [],
            "expected_answer": None,
            "required_hops": 0,
            "expected_citation_type": "none",
        },
        {
            "id": "negative_006",
            "question": "How is Shakespeare connected to artificial intelligence?",
            "expected_entities": [],
            "expected_relationships": [],
            "expected_answer": None,
            "required_hops": 0,
            "expected_citation_type": "none",
        },
        {
            "id": "negative_007",
            "question": "Who developed quantum computing?",
            "expected_entities": [],
            "expected_relationships": [],
            "expected_answer": None,
            "required_hops": 0,
            "expected_citation_type": "none",
        },
        {
            "id": "negative_008",
            "question": "What did Steve Jobs discover?",
            "expected_entities": [],
            "expected_relationships": [],
            "expected_answer": None,
            "required_hops": 0,
            "expected_citation_type": "none",
        },
        {
            "id": "negative_009",
            "question": "How is Mars related to Einstein?",
            "expected_entities": [],
            "expected_relationships": [],
            "expected_answer": None,
            "required_hops": 0,
            "expected_citation_type": "none",
        },
        {
            "id": "negative_010",
            "question": "Who discovered DNA?",
            "expected_entities": [],
            "expected_relationships": [],
            "expected_answer": None,
            "required_hops": 0,
            "expected_citation_type": "none",
        },
    ]

def main() -> None:
    dataset = build_dataset()
    save_dataset(dataset)

    counts = {}

    for item in dataset:
        category = f"{item['required_hops']}-hop"
        counts[category] = counts.get(category, 0) + 1

    print(f"Generated benchmark: {OUTPUT_PATH}")
    print(f"Total questions: {len(dataset)}")

    for category, count in counts.items():
        print(f"{category}: {count}")


if __name__ == "__main__":
    main()