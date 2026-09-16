from reasoning.models import ReasoningChain


def calculate_chain_confidence(
    chain: ReasoningChain,
    query_entities: list[str],
    expected_relationships: list[str],
) -> float:
    score = 0.0

    nodes = [chain.start]

    for step in chain.steps:
        nodes.append(step.target)

    for entity in query_entities:
        if any(
            entity.lower() in node.lower()
            for node in nodes
        ):
            score += 0.3

    relationships = [
        step.relationship.lower()
        for step in chain.steps
    ]

    for relationship in expected_relationships:
        if relationship.lower() in relationships:
            score += 0.3

    hop_count = len(relationships)

    if hop_count == 1:
        score += 0.2
    elif hop_count == 2:
        score += 0.15
    else:
        score += 0.1

    return min(score, 1.0)