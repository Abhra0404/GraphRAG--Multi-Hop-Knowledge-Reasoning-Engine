DOCUMENT_METADATA = {
    "paper.pdf": {
        "title": "SWISH: A SELF-GATED ACTIVATION FUNCTION",
        "authors": [
            "Prajit Ramachandran",
            "Barret Zoph",
            "Quoc V. Le",
        ],
        "organization": "Google Brain",
    }
}


def get_document_metadata(source: str) -> dict:
    return DOCUMENT_METADATA.get(
        source,
        {
            "title": source,
            "authors": [],
            "organization": None,
        },
    )