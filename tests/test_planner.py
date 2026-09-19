from reasoning.planner import plan_query


def main():
    queries = [
        "What did Albert Einstein develop?",
        "What does the theory of relativity describe?",
        "What does Einstein's work tell us about spacetime?",
    ]

    for query in queries:
        print("\n--- Query ---")
        print(query)

        print("\n--- Plan ---")
        print(plan_query(query))


if __name__ == "__main__":
    main()