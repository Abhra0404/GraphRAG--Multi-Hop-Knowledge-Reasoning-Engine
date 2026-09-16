from retrieval.pipeline import answer_query


def main():
    query = "How do knowledge graphs represent information?"

    result = answer_query(query)

    print("\n--- Answer ---")
    print(result["answer"])

    print("\n--- Sources ---")

    for source in result["sources"]:
        print(source)


if __name__ == "__main__":
    main()