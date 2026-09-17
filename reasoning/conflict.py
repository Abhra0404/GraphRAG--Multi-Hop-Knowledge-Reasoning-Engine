def detect_conflicts(
    vector_results: list,
    graph_results: list[dict],
) -> list[dict]:
    conflicts = []

    graph_facts = set()

    for path in graph_results:
        nodes = path.get("nodes", [])
        relationships = path.get("relationships", [])

        for source, relationship, target in zip(
            nodes,
            relationships,
            nodes[1:],
        ):
            graph_facts.add(
                (
                    source.lower(),
                    relationship.upper(),
                    target.lower(),
                )
            )

    for result in vector_results:
        content = result.payload.get(
            "content",
            "",
        ).lower()

        for source, relationship, target in graph_facts:
            if source in content and target not in content:
                conflicts.append(
                    {
                        "type": "potential_conflict",
                        "source": source,
                        "relationship": relationship,
                        "graph_target": target,
                        "text": result.payload.get(
                            "content",
                            "",
                        ),
                    }
                )

    return conflicts