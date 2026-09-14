from retrieval.vector import retrieve


def main():
    query = "How do knowledge graphs represent information?"

    results = retrieve(query, limit=3)

    for index, result in enumerate(results, start=1):
        print(f"\n--- Result {index} ---")
        print(f"Score: {result.score}")
        print(result.payload["content"])


if __name__ == "__main__":
    main()