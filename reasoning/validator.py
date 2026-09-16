from reasoning.models import ReasoningChain


def validate_chain(
    chain: ReasoningChain,
) -> bool:
    if not chain.start:
        return False

    if not chain.steps:
        return False

    for step in chain.steps:
        if not step.relationship:
            return False

        if not step.target:
            return False

    return True


def validate_chains(
    chains: list[ReasoningChain],
) -> list[ReasoningChain]:
    return [
        chain
        for chain in chains
        if validate_chain(chain)
    ]