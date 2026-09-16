from retrieval.graph import retrieve_graph


def main():
    results = retrieve_graph("Albert Einstein")

    print("\n--- Graph Results ---")

    for result in results:
        print(result)


if __name__ == "__main__":
    main()