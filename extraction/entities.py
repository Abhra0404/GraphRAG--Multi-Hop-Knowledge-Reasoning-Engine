import json

from generation.llm import llm_client


ENTITY_PROMPT = """
Extract the important entities from the text.

Return ONLY valid JSON in this format:

{{
  "entities": [
    {{
      "name": "entity name",
      "type": "entity type"
    }}
  ]
}}

Text:
{text}
""".strip()


def extract_entities(text: str) -> list[dict]:
    prompt = ENTITY_PROMPT.format(text=text)

    response = llm_client.generate(prompt)

    try:
        data = json.loads(response)
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"LLM returned invalid entity JSON: {response}"
        ) from exc

    return data.get("entities", [])