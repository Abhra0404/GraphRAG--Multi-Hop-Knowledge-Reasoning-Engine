from retrieval.hybrid import hybrid_retrieve


def main():
    query = "What does Einstein's work tell us about spacetime?"

    results = hybrid_retrieve(query)

    print("\n--- Query Plan ---")
    print(results["plan"])

    print("\n--- Vector Results ---")

    for result in results["vector"]:
        print({
            "score": result.score,
            "source": result.payload.get("source"),
            "chunk_index": result.payload.get("chunk_index"),
        })

    print("\n--- Graph Results ---")

    for result in results["graph"]:
        print(result)


if __name__ == "__main__":
    main()