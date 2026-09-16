from reasoning.models import (
    EvidenceBundle,
    ReasoningChain,
    TextEvidence,
)


def rank_text_evidence(
    evidence: list[TextEvidence],
) -> list[TextEvidence]:
    return sorted(
        evidence,
        key=lambda item: item.score,
        reverse=True,
    )


def rank_reasoning_chains(
    chains: list[ReasoningChain],
) -> list[ReasoningChain]:
    return sorted(
        chains,
        key=lambda item: item.confidence,
        reverse=True,
    )


def fuse_evidence(
    text_evidence: list,
    reasoning_chains: list[ReasoningChain],
) -> EvidenceBundle:
    text_items = []

    for result in text_evidence:
        payload = result.payload

        text_items.append(
            TextEvidence(
                content=payload.get(
                    "content",
                    "",
                ),
                source=payload.get(
                    "source",
                    "unknown",
                ),
                chunk_index=payload.get(
                    "chunk_index"
                ),
                score=getattr(
                    result,
                    "score",
                    0.0,
                ),
            )
        )

    ranked_text = rank_text_evidence(
        text_items
    )

    ranked_chains = rank_reasoning_chains(
        reasoning_chains
    )

    return EvidenceBundle(
        text=ranked_text,
        chains=ranked_chains,
    )