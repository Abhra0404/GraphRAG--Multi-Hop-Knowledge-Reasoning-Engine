from generation.llm import llm_client
from generation.prompt import build_prompt


def main():
    prompt = build_prompt(
        query="What is a knowledge graph?",
        context=(
            "A knowledge graph represents information using entities "
            "and relationships between those entities."
        ),
    )

    answer = llm_client.generate(prompt)

    print("\n--- Answer ---")
    print(answer)


if __name__ == "__main__":
    main()