def score_path(
    path: dict,
    query_entities: list[str],
) -> float:
    nodes = [
        node.lower()
        for node in path.get("nodes", [])
    ]

    relationships = [
        relationship.lower()
        for relationship in path.get("relationships", [])
    ]

    query_entities_lower = [
        entity.lower()
        for entity in query_entities
    ]

    score = 0.0

    # Reward query entities appearing in the path
    for entity in query_entities_lower:
        if any(entity in node for node in nodes):
            score += 3.0

    # Strongly reward paths connecting multiple query entities
    matched_entities = sum(
        any(entity in node for node in nodes)
        for entity in query_entities_lower
    )

    if matched_entities >= 2:
        score += 5.0

    # Prefer shorter paths
    score -= max(len(relationships) - 1, 0) * 0.5

    # Reward meaningful relationships
    useful_relationships = {
        "developed",
        "describes",
        "related_to",
        "created",
        "discovered",
        "works_on",
    }

    for relationship in relationships:
        if relationship in useful_relationships:
            score += 1.0

    return score


def rank_paths(
    paths: list[dict],
    query_entities: list[str],
    limit: int = 5,
) -> list[dict]:
    scored_paths = []

    for path in paths:
        score = score_path(
            path,
            query_entities,
        )

        scored_paths.append(
            {
                **path,
                "score": score,
            }
        )

    scored_paths.sort(
        key=lambda path: path["score"],
        reverse=True,
    )

    return scored_paths[:limit]