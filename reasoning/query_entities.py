import json

from generation.llm import llm_client


QUERY_ENTITY_PROMPT = """
Identify the entities in the user's question that could be searched
in a knowledge graph.

Return ONLY valid JSON:

{{
  "entities": [
    "entity name"
  ]
}}

Question:
{query}
""".strip()


def extract_query_entities(query: str) -> list[str]:
    prompt = QUERY_ENTITY_PROMPT.format(query=query)

    response = llm_client.generate(prompt)

    try:
        data = json.loads(response)
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"LLM returned invalid query entity JSON: {response}"
        ) from exc

    return data.get("entities", [])