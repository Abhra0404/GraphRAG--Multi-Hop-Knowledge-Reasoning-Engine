from reasoning.chain import deduplicate_chains
from reasoning.confidence import calculate_chain_confidence
from reasoning.models import ReasoningChain
from reasoning.validator import validate_chains


def _matches_entity(
    node: str,
    entity: str,
) -> bool:
    return entity.lower() in node.lower()


def _connects_query_entities(
    chain: ReasoningChain,
    query_entities: list[str],
) -> bool:
    if len(query_entities) < 2:
        return True

    nodes = [chain.start]

    for step in chain.steps:
        nodes.append(step.target)

    matched = sum(
        any(
            _matches_entity(node, entity)
            for node in nodes
        )
        for entity in query_entities
    )

    return matched >= 2


def _matches_expected_relationships(
    chain: ReasoningChain,
    expected_relationships: list[str],
) -> bool:
    if not expected_relationships:
        return True

    relationships = [
        step.relationship
        for step in chain.steps
    ]

    return any(
        expected.lower() in relationship.lower()
        for expected in expected_relationships
        for relationship in relationships
    )


def build_valid_reasoning_chains(
    chains: list[ReasoningChain],
    query_entities: list[str],
    expected_relationships: list[str] | None = None,
) -> list[ReasoningChain]:

    chains = validate_chains(chains)
    chains = deduplicate_chains(chains)

    expected_relationships = (
        expected_relationships or []
    )

    valid_chains = [
        chain
        for chain in chains
        if _connects_query_entities(
            chain,
            query_entities,
        )
        and _matches_expected_relationships(
            chain,
            expected_relationships,
        )
    ]

    for chain in valid_chains:
        chain.confidence = calculate_chain_confidence(
            chain,
            query_entities,
            expected_relationships,
        )

    valid_chains.sort(
        key=lambda chain: chain.confidence,
        reverse=True,
    )

    return valid_chains