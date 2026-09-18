from reasoning.models import (
    ReasoningChain,
    TextEvidence,
)


def format_graph_path(path: dict) -> str:
    nodes = path.get("nodes", [])
    relationships = path.get("relationships", [])

    if not nodes:
        return ""

    parts = [nodes[0]]

    for relationship, node in zip(
        relationships,
        nodes[1:],
    ):
        parts.append(f"--[{relationship}]-->")
        parts.append(node)

    return " ".join(parts)


def format_reasoning_chain(
    chain: ReasoningChain,
) -> str:
    if not chain.start:
        return ""

    parts = [chain.start]

    for step in chain.steps:
        relationship = step.relationship
        target = step.target

        if step.source_document is not None:
            source_text = (
                f"{step.source_document}, "
                f"chunk {step.source_chunk}"
            )
        else:
            source_text = "unknown"

        parts.append(
            f"--[{relationship}]-->"
        )

        parts.append(
            f"{target} "
            f"(source: {source_text})"
        )

    return " ".join(parts)


def format_metadata(metadata: dict) -> str:
    title = metadata.get("title")
    authors = metadata.get("authors", [])
    organization = metadata.get("organization")

    lines = []

    if title:
        lines.append(f"Title: {title}")

    if authors:
        lines.append(
            "Authors: " + ", ".join(authors)
        )

    if organization:
        lines.append(
            f"Organization: {organization}"
        )

    return "\n".join(lines)


def build_evidence(
    text_evidence: list[TextEvidence],
    graph_results: list[dict],
    reasoning_chains: list[ReasoningChain] | None = None,
    metadata: dict | None = None,
) -> str:
    sections = []

    # -------------------------
    # Document Metadata
    # -------------------------

    if metadata:
        metadata_text = format_metadata(metadata)

        if metadata_text:
            sections.append(
                "DOCUMENT METADATA:\n"
                "[Metadata 1]\n"
                f"{metadata_text}"
            )

    # -------------------------
    # Text Evidence
    # -------------------------

    if text_evidence:
        sections.append("TEXT EVIDENCE:")

        for index, evidence in enumerate(
            text_evidence,
            start=1,
        ):
            sections.append(
                f"[Text {index}] "
                f"Source: {evidence.source}, "
                f"chunk {evidence.chunk_index}, "
                f"score: {evidence.score:.4f}\n"
                f"{evidence.content}"
            )

    # -------------------------
    # Reasoning Chains
    # -------------------------

    if reasoning_chains:
        sections.append(
            "\nREASONING CHAINS:"
        )

        for index, chain in enumerate(
            reasoning_chains,
            start=1,
        ):
            formatted_chain = (
                format_reasoning_chain(chain)
            )

            if formatted_chain:
                sections.append(
                    f"[Chain {index}] "
                    f"Confidence: "
                    f"{chain.confidence:.2f}\n"
                    f"{formatted_chain}"
                )

    # -------------------------
    # Fallback Graph Evidence
    # -------------------------

    elif graph_results:
        sections.append(
            "\nGRAPH EVIDENCE:"
        )

        for index, path in enumerate(
            graph_results,
            start=1,
        ):
            formatted_path = (
                format_graph_path(path)
            )

            if formatted_path:
                sections.append(
                    f"[Path {index}] "
                    f"{formatted_path}"
                )

    return "\n\n".join(sections)