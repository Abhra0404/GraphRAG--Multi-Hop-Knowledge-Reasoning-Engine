import re


def normalize_text(text: str) -> str:
    text = text.lower()
    text = text.replace("\u202f", " ")
    text = text.replace("\u00a0", " ")
    text = re.sub(r"[^a-z0-9\s]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def answer_contains_expected(
    answer: str,
    expected_answer: str | None,
) -> bool:
    normalized_answer = normalize_text(answer)

    if expected_answer is None:
        insufficient_patterns = [
            "not enough information",
            "insufficient information",
            "do not have enough information",
            "cannot answer",
            "no information",
        ]

        return any(
            pattern in normalized_answer
            for pattern in insufficient_patterns
        )

    normalized_expected = normalize_text(expected_answer)

    if normalized_expected in normalized_answer:
        return True

    expected_parts = normalized_expected.split(" which ")

    return all(
        part in normalized_answer
        for part in expected_parts
    )


def entity_recall(
    detected_entities: list[str],
    expected_entities: list[str],
) -> float:
    if not expected_entities:
        return 1.0

    detected = [entity.lower() for entity in detected_entities]

    matched = sum(
        any(
            expected.lower() in entity
            or entity in expected.lower()
            for entity in detected
        )
        for expected in expected_entities
    )

    return matched / len(expected_entities)


def relationship_recall(
    detected_relationships: list[str],
    expected_relationships: list[str],
) -> float:
    if not expected_relationships:
        return 1.0

    detected = [
        relationship.lower()
        for relationship in detected_relationships
    ]

    matched = sum(
        any(
            expected.lower() == relationship
            for relationship in detected
        )
        for expected in expected_relationships
    )

    return matched / len(expected_relationships)


def reasoning_chain_recall(
    chains: list,
    expected_relationships: list[str],
    required_hops: int,
) -> float:
    if not expected_relationships:
        return 1.0 if not chains else 0.0

    for chain in chains:
        relationships = [
            step.relationship.upper()
            for step in chain.steps
        ]

        if len(relationships) != required_hops:
            continue

        if all(
            expected.upper() in relationships
            for expected in expected_relationships
        ):
            return 1.0

    return 0.0


def citation_recall(
    answer: str,
    available_citations: list[str],
) -> float:
    if not available_citations:
        return 1.0

    normalized_answer = answer.replace(
        "\u202f",
        " ",
    ).replace(
        "\u00a0",
        " ",
    )

    cited = sum(
        citation in normalized_answer
        for citation in available_citations
    )

    return cited / len(available_citations)

from embeddings.embedder import embed_texts


def semantic_answer_similarity(
    answer: str,
    expected_answer: str | None,
) -> float:
    if expected_answer is None:
        return 1.0 if answer_contains_expected(
            answer,
            None,
        ) else 0.0

    embeddings = embed_texts(
        [
            normalize_text(answer),
            normalize_text(expected_answer),
        ]
    )

    similarity = sum(
        a * b
        for a, b in zip(
            embeddings[0],
            embeddings[1],
        )
    )

    return similarity