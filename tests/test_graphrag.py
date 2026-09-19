from reasoning.pipeline import answer_query


def main():
    query = "What does Einstein's work tell us about spacetime?"

    result = answer_query(query)

    print("\n--- Answer ---")
    print(result["answer"])

    print("\n--- Detected Entities ---")
    print(result["entities"])

    print("\n--- Evidence ---")
    print(result["evidence"])


if __name__ == "__main__":
    main()