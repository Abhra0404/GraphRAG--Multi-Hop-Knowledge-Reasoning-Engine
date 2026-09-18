RELATIONS = [
    # Einstein chain
    ("Albert Einstein", "DEVELOPED", "theory of relativity"),
    ("theory of relativity", "DESCRIBES", "spacetime"),
    ("spacetime", "MODELS", "gravity"),
    ("gravity", "AFFECTS", "matter"),

    # Newton chain
    ("Isaac Newton", "DEVELOPED", "laws of motion"),
    ("laws of motion", "DESCRIBES", "forces"),
    ("forces", "AFFECT", "movement"),
    ("movement", "OCCURS_IN", "spacetime"),

    # Curie chain
    ("Marie Curie", "DISCOVERED", "radioactivity"),
    ("radioactivity", "RELATED_TO", "nuclear physics"),
    ("nuclear physics", "STUDIES", "atomic nuclei"),
    ("atomic nuclei", "CONTAIN", "protons"),

    # Tesla / Maxwell chain
    ("Nikola Tesla", "WORKED_ON", "electrical engineering"),
    ("electrical engineering", "USES", "electromagnetism"),
    ("James Clerk Maxwell", "DEVELOPED", "electromagnetism"),
    ("electromagnetism", "DESCRIBES", "electric fields"),
    ("electric fields", "AFFECT", "charged particles"),

    # Computing chain
    ("Ada Lovelace", "WORKED_ON", "mathematical computing"),
    ("mathematical computing", "INFLUENCED", "computing"),
    ("Alan Turing", "WORKED_ON", "computing"),
    ("computing", "INFLUENCED", "artificial intelligence"),
    ("artificial intelligence", "USES", "machine learning"),
    ("machine learning", "USES", "neural networks"),

    # Darwin chain
    ("Charles Darwin", "DEVELOPED", "evolution"),
    ("evolution", "EXPLAINS", "natural selection"),
    ("natural selection", "AFFECTS", "populations"),
    ("populations", "CHANGE_OVER_TIME", "species"),

    # Space science chain
    ("Katherine Johnson", "WORKED_ON", "space science"),
    ("space science", "USES", "mathematics"),
    ("mathematics", "SUPPORTS", "scientific modeling"),
    ("scientific modeling", "USES", "computing"),

    # Grace Hopper / computing connection
    ("Grace Hopper", "WORKED_ON", "computing"),
    ("computing", "ENABLES", "software"),
    ("software", "RUNS_ON", "computers"),

    # Cross-domain connections — important for multi-hop reasoning
    ("theory of relativity", "INFLUENCED", "modern physics"),
    ("modern physics", "USES", "mathematics"),
    ("mathematics", "SUPPORTS", "machine learning"),
]