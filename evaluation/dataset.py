EVALUATION_DATASET = [
    {
        "id": "single_hop_001",
        "question": "What did Albert Einstein develop?",
        "expected_entities": ["Albert Einstein"],
        "expected_relationships": ["DEVELOPED"],
        "expected_answer": "Albert Einstein developed the theory of relativity.",
        "required_hops": 1,
        "expected_citation_type": "chain"
    },
    {
        "id": "single_hop_002",
        "question": "What does the theory of relativity describe?",
        "expected_entities": ["theory of relativity"],
        "expected_relationships": ["DESCRIBES"],
        "expected_answer": "The theory of relativity describes spacetime.",
        "required_hops": 1,
        "expected_citation_type": "chain"
    },
    {
        "id": "multi_hop_001",
        "question": "What does Einstein's work tell us about spacetime?",
        "expected_entities": ["Albert Einstein", "spacetime"],
        "expected_relationships": ["DEVELOPED", "DESCRIBES"],
        "expected_answer": (
            "Einstein developed the theory of relativity, "
            "which describes spacetime."
        ),
        "required_hops": 2,
        "expected_citation_type": "chain"
    },
    {
        "id": "insufficient_001",
        "question": "Who discovered quantum mechanics?",
        "expected_entities": [],
        "expected_relationships": [],
        "expected_answer": None,
        "required_hops": 0,
        "expected_citation_type": "none"
    },
]