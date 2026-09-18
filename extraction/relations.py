import json
import re

from generation.llm import llm_client


RELATION_PROMPT = """
Extract relationships from the provided text.

Return ONLY valid JSON:

{{
  "relations": [
    {{
      "source": "entity A",
      "relation": "RELATION_TYPE",
      "target": "entity B"
    }}
  ]
}}

Rules:
- Only use entities from the provided entity list.
- Do not invent entities.
- Use concise uppercase relationship names.
- Extract only relationships explicitly supported by the text.
- If there are no relationships, return {{"relations": []}}.
- Keep the response short.
- Do not explain your answer.

Entities:
{entities}

Text:
{text}
""".strip()


def _extract_json(response: str) -> dict:
    response = response.strip()

    # Remove markdown code fences.
    response = re.sub(r"^```(?:json)?", "", response, flags=re.IGNORECASE)
    response = re.sub(r"```$", "", response)
    response = response.strip()

    start = response.find("{")
    end = response.rfind("}")

    if start == -1 or end == -1 or end <= start:
        raise ValueError("No JSON object found.")

    return json.loads(response[start : end + 1])


def extract_relations(
    text: str,
    entities: list[dict],
) -> list[dict]:

    if not entities:
        return []

    entity_names = [
        entity["name"]
        for entity in entities
        if isinstance(entity, dict) and entity.get("name")
    ]

    if not entity_names:
        return []

    prompt = RELATION_PROMPT.format(
        entities=json.dumps(
            entity_names,
            ensure_ascii=False,
        ),
        text=text,
    )

    response = llm_client.generate(prompt)

    try:
        data = _extract_json(response)

    except (json.JSONDecodeError, ValueError) as exc:
        print(
            "Warning: invalid relation JSON. "
            f"Skipping relation extraction: {exc}"
        )
        print(f"Response preview: {response[:300]}")
        return []

    relations = data.get("relations", [])

    if not isinstance(relations, list):
        return []

    allowed_entities = {
        entity.lower()
        for entity in entity_names
    }

    valid_relations = []

    for relation in relations:
        if not isinstance(relation, dict):
            continue

        source = relation.get("source")
        relation_type = relation.get("relation")
        target = relation.get("target")

        if not all(
            isinstance(value, str) and value.strip()
            for value in (source, relation_type, target)
        ):
            continue

        source = source.strip()
        target = target.strip()
        relation_type = relation_type.strip().upper()

        if source.lower() not in allowed_entities:
            continue

        if target.lower() not in allowed_entities:
            continue

        valid_relations.append(
            {
                "source": source,
                "relation": relation_type,
                "target": target,
            }
        )

    return valid_relations