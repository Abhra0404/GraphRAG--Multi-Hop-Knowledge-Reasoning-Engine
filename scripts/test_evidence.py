from reasoning.evidence import build_evidence
from retrieval.hybrid import hybrid_retrieve


def main():
    results = hybrid_retrieve(
        "What did Albert Einstein develop?"
    )

    evidence = build_evidence(
        vector_results=results["vector"],
        graph_results=results["graph"],
    )

    print("\n--- FUSED EVIDENCE ---")
    print(evidence)


if __name__ == "__main__":
    main()