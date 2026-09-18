import json
import re
from pathlib import Path


BASE_DIR = Path(__file__).parent
RESULTS_FILE = BASE_DIR / "results.json"
EVALUATION_FILE = BASE_DIR / "evaluation_results.json"


REFERENCE_ANSWERS = {
    "swish_01": ["x * sigmoid(x)", "x · sigmoid(x)"],
    "swish_02": ["ReLU"],
    "swish_03": [
        "Prajit Ramachandran",
        "Barret Zoph",
        "Quoc V. Le",
    ],
    "swish_04": ["f(x) = x", "sigmoid(x)"],
    "swish_05": [
        "replacement",
        "ReLU",
        "pointwise",
        "self-gating",
    ],
    "swish_06": ["alternative", "ReLU"],
    "swish_07": ["ReLU", "activation function"],
    "swish_08": ["outperform", "ReLU"],
    "swish_09": [
        "ResNet",
        "Inception-ResNet",
        "Transformer",
    ],
    "swish_10": ["non-monotonic", "smooth", "ReLU"],
    "swish_11": ["Swish", "activation function", "performance"],
    "swish_12": ["x", "sigmoid", "ReLU", "performance"],
    "swish_13": ["replace", "ReLU", "Swish"],
    "swish_14": ["activation", "performance", "models"],
    "swish_15": ["Swish", "outperform", "activation functions"],
}


def normalize(text: str) -> str:
    text = text.lower()
    text = text.replace("·", "*")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def check_reference_answer(
    answer: str,
    expected_terms: list[str],
) -> bool:
    answer = normalize(answer)

    matched = 0

    for term in expected_terms:
        if normalize(term) in answer:
            matched += 1

    # Require at least half of the expected concepts.
    required = max(1, len(expected_terms) // 2)

    return matched >= required


def check_citations(answer: str) -> bool:
    return bool(
        re.search(
            r"\[(?:Text|Chain|Path|Metadata)\s+\d+\]",
            answer,
            re.IGNORECASE,
        )
    )


def check_graph_usage(result: dict) -> bool:
    chains = result.get("graphrag", {}).get(
        "reasoning_chains",
        [],
    )

    evidence = result.get("graphrag", {}).get(
        "evidence",
        "",
    )

    return bool(
        chains
        or "GRAPH EVIDENCE:" in evidence
        or "[Path " in evidence
    )


def evaluate_result(result: dict) -> dict:
    result_id = result["id"]

    answer = result.get("graphrag", {}).get(
        "answer",
        "",
    )

    expected = REFERENCE_ANSWERS.get(
        result_id,
        [],
    )

    return {
        "id": result_id,
        "type": result["type"],
        "correct": check_reference_answer(
            answer,
            expected,
        ),
        "citation_present": check_citations(answer),
        "graph_evidence_used": check_graph_usage(result),
    }


def main():
    with open(RESULTS_FILE, encoding="utf-8") as file:
        results = json.load(file)

    evaluations = [
        evaluate_result(result)
        for result in results
        if result.get("status") == "success"
    ]

    total = len(evaluations)

    correctness = sum(
        item["correct"]
        for item in evaluations
    )

    citations = sum(
        item["citation_present"]
        for item in evaluations
    )

    graph_usage = sum(
        item["graph_evidence_used"]
        for item in evaluations
    )

    report = {
        "total_cases": total,
        "answer_correctness": (
            correctness / total if total else 0
        ),
        "citation_presence": (
            citations / total if total else 0
        ),
        "graph_evidence_usage": (
            graph_usage / total if total else 0
        ),
        "cases": evaluations,
    }

    with open(
        EVALUATION_FILE,
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            report,
            file,
            indent=2,
            ensure_ascii=False,
        )

    print("Real-paper evaluation")
    print("---------------------")
    print(f"Cases:              {total}")
    print(
        f"Answer correctness: "
        f"{report['answer_correctness']:.2%}"
    )
    print(
        f"Citation presence:  "
        f"{report['citation_presence']:.2%}"
    )
    print(
        f"Graph evidence:     "
        f"{report['graph_evidence_usage']:.2%}"
    )
    print()
    print(f"Saved: {EVALUATION_FILE}")


if __name__ == "__main__":
    main()