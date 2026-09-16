import json

from generation.llm import llm_client


RELATION_PROMPT = """
Extract meaningful relationships between the entities in the text.

Return ONLY valid JSON in this format:

{{
  "relations": [
    {{
      "source": "entity A",
      "relation": "RELATION_TYPE",
      "target": "entity B"
    }}
  ]
}}

Text:
{text}

Entities:
{entities}
""".strip()


def extract_relations(
    text: str,
    entities: list[dict],
) -> list[dict]:
    prompt = RELATION_PROMPT.format(
        text=text,
        entities=json.dumps(entities),
    )

    response = llm_client.generate(prompt)

    try:
        data = json.loads(response)
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"LLM returned invalid relation JSON: {response}"
        ) from exc

    return data.get("relations", [])