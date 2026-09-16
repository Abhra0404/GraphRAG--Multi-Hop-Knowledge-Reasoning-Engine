import json
import re

from generation.llm import llm_client


PLANNER_PROMPT = """
You are a query planner for a knowledge graph.

Analyze the user's question and return ONLY valid JSON:

{{
  "entities": ["entity 1", "entity 2"],
  "intent": "short description of what the user wants",
  "relationship_types": ["RELATION_TYPE"]
}}

Rules:
- Extract only entities relevant to answering the question.
- Identify relationship types that are likely relevant to answering the question.
- Use concise uppercase relationship names.
- Do not determine the number of graph hops.

Question:
{query}
""".strip()


def _estimate_hops(query: str) -> int:
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

    return 1


def plan_query(query: str) -> dict:
    prompt = PLANNER_PROMPT.format(query=query)

    response = llm_client.generate(prompt)

    try:
        plan = json.loads(response)
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"LLM returned invalid query plan: {response}"
        ) from exc

    return {
        "entities": plan.get("entities", []),
        "intent": plan.get("intent", ""),
        "relationship_types": plan.get(
            "relationship_types",
            [],
        ),
        "max_hops": max(
            1,
            min(3, _estimate_hops(query)),
        ),
    }

