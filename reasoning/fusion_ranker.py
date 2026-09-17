def normalize_score(
    score: float,
    minimum: float,
    maximum: float,
) -> float:
    if maximum == minimum:
        return 1.0

    return (score - minimum) / (
        maximum - minimum
    )


def fuse_scores(
    vector_score: float,
    graph_score: float,
    vector_weight: float = 0.4,
    graph_weight: float = 0.6,
) -> float:
    return (
        vector_score * vector_weight
        + graph_score * graph_weight
    )


def rank_fused_evidence(
    vector_results: list,
    graph_results: list[dict],
    limit: int = 10,
) -> list[dict]:

    fused = []

    vector_scores = [
        getattr(result, "score", 0.0)
        for result in vector_results
    ]

    if vector_scores:
        vector_min = min(vector_scores)
        vector_max = max(vector_scores)
    else:
        vector_min = vector_max = 0.0

    for result in vector_results:
        score = getattr(result, "score", 0.0)

        fused.append(
            {
                "type": "text",
                "content": result.payload.get(
                    "content",
                    "",
                ),
                "source": result.payload.get(
                    "source",
                    "unknown",
                ),
                "chunk_index": result.payload.get(
                    "chunk_index",
                ),
                "score": normalize_score(
                    score,
                    vector_min,
                    vector_max,
                ),
            }
        )

    graph_scores = [
        path.get("score", 0.0)
        for path in graph_results
    ]

    if graph_scores:
        graph_min = min(graph_scores)
        graph_max = max(graph_scores)
    else:
        graph_min = graph_max = 0.0

    for path in graph_results:
        graph_score = path.get("score", 0.0)

        normalized_graph_score = normalize_score(
            graph_score,
            graph_min,
            graph_max,
        )

        fused.append(
            {
                "type": "graph",
                "path": path,
                "score": normalized_graph_score,
            }
        )

    fused.sort(
        key=lambda item: item["score"],
        reverse=True,
    )

    return fused[:limit]