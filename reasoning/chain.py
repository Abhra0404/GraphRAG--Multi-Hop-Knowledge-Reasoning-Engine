from reasoning.models import ReasoningChain, ReasoningStep


def build_reasoning_chains(
    ranked_paths: list[dict],
) -> list[ReasoningChain]:
    chains = []

    for path in ranked_paths:
        nodes = path.get("nodes", [])
        relationships = path.get("relationships", [])
        sources = path.get("sources", [])
        chunks = path.get("chunks", [])

        if len(nodes) < 2:
            continue

        steps = []

        for index, (relationship, target) in enumerate(
            zip(
                relationships,
                nodes[1:],
            )
        ):
            steps.append(
                ReasoningStep(
                    relationship=relationship,
                    target=target,
                    source_document=(
                        sources[index]
                        if index < len(sources)
                        else None
                    ),
                    source_chunk=(
                        chunks[index]
                        if index < len(chunks)
                        else None
                    ),
                )
            )

        chains.append(
            ReasoningChain(
                start=nodes[0],
                steps=steps,
                score=path.get("score", 0.0),
            )
        )

    return chains


def deduplicate_chains(
    chains: list[ReasoningChain],
) -> list[ReasoningChain]:
    seen = set()
    unique = []

    for chain in chains:
        nodes = [chain.start]

        for step in chain.steps:
            nodes.append(step.target)

        key = tuple(nodes)

        if key in seen:
            continue

        seen.add(key)
        unique.append(chain)

    return unique