import json
from pathlib import Path

from reasoning.pipeline import answer_query
from retrieval.vector import retrieve


BASE_DIR = Path(__file__).parent
QUESTIONS_FILE = BASE_DIR / "swish_questions.json"
RESULTS_FILE = BASE_DIR / "results.json"


def load_questions():
    with open(QUESTIONS_FILE, encoding="utf-8") as file:
        return json.load(file)


def run_vanilla(question: str) -> dict:
    results = retrieve(question, limit=5)

    evidence = "\n\n".join(
        result.payload.get("content", "")
        for result in results
        if result.payload
    )

    return {
        "evidence": evidence,
        "evidence_count": len(results),
    }


def run_graphrag(question: str) -> dict:
    result = answer_query(question)

    return {
        "answer": result["answer"],
        "entities": result["entities"],
        "evidence": result["evidence"],
        "reasoning_chains": [
            chain.model_dump()
            for chain in result["reasoning_chains"]
        ],
    }


def main():
    questions = load_questions()
    results = []

    print(f"Running {len(questions)} real-paper questions...\n")

    for index, item in enumerate(questions, start=1):
        question = item["question"]

        print(f"[{index}/{len(questions)}] {question}")

        try:
            vanilla = run_vanilla(question)
            graphrag = run_graphrag(question)

            results.append(
                {
                    **item,
                    "vanilla": vanilla,
                    "graphrag": graphrag,
                    "status": "success",
                }
            )

            print("  ✓ completed")

        except Exception as exc:
            results.append(
                {
                    **item,
                    "status": "failed",
                    "error": f"{type(exc).__name__}: {exc}",
                }
            )

            print(f"  ✗ failed: {exc}")

    with open(RESULTS_FILE, "w", encoding="utf-8") as file:
        json.dump(results, file, indent=2, ensure_ascii=False)

    successful = sum(
        result["status"] == "success"
        for result in results
    )

    print()
    print("Evaluation complete.")
    print(f"Successful: {successful}/{len(results)}")
    print(f"Results: {RESULTS_FILE}")


if __name__ == "__main__":
    main()