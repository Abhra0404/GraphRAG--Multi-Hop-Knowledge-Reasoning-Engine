import json
import re

from generation.llm import llm_client


PLANNER_PROMPT = """
You are a query planner for a knowledge graph.

Return ONLY a JSON object. Do not provide explanations, markdown, or
text before or after the JSON.

Format:

{{
  "entities": ["entity 1", "entity 2"],
  "intent": "short description",
  "relationship_types": ["RELATION_TYPE"],
  "sub_queries": [
    "simple sub-question 1",
    "simple sub-question 2"
  ]
}}

Rules:
- Extract only entities relevant to answering the question.
- Identify relationship types likely relevant to answering the question.
- Break complex questions into simple sub-questions.
- Keep simple questions to one sub-query.
- Use concise uppercase relationship names.
- Do not determine graph hops.
- If no graph relationship is relevant, use an empty relationship_types list.

Question:
{query}
""".strip()


def _extract_json(response: str) -> dict:
    response = response.strip()

    # Remove markdown code fences.
    response = re.sub(
        r"```(?:json)?",
        "",
        response,
        flags=re.IGNORECASE,
    )
    response = response.replace("```", "").strip()

    # Find the JSON object even if the model added explanations.
    start = response.find("{")
    end = response.rfind("}")

    if start == -1 or end == -1 or end <= start:
        raise ValueError(
            f"LLM returned no JSON object: {response}"
        )

    json_text = response[start : end + 1]

    try:
        return json.loads(json_text)
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"LLM returned invalid query plan: {response}"
        ) from exc


def _estimate_hops(
    query: str,
    sub_queries: list[str] | None = None,
) -> int:
    query_lower = query.lower()

    multi_hop_patterns = [
        r"\bhow\b.*\brelated\b",
        r"\bconnection\b",
        r"\bconnect\b",
        r"\bthrough\b",
        r"\bbetween\b",
        r"\bwork\b.*\babout\b",
        r"\bcontribution\b",
        r"\bimpact\b",
    ]

    for pattern in multi_hop_patterns:
        if re.search(pattern, query_lower):
            return 2

    if sub_queries and len(sub_queries) > 1:
        return 2

    return 1


def plan_query(query: str) -> dict:
    prompt = PLANNER_PROMPT.format(query=query)

    response = llm_client.generate(prompt)

    plan = _extract_json(response)

    sub_queries = plan.get("sub_queries", [])

    if not isinstance(sub_queries, list) or not sub_queries:
        sub_queries = [query]

    return {
        "entities": plan.get("entities", []),
        "intent": plan.get("intent", ""),
        "relationship_types": plan.get(
            "relationship_types",
            [],
        ),
        "sub_queries": sub_queries,
        "max_hops": max(
            1,
            min(
                3,
                _estimate_hops(query, sub_queries),
            ),
        ),
    }