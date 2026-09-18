def build_prompt(query: str, context: str) -> str:
    return f"""
You are a precise knowledge reasoning assistant.

Answer the user's question using ONLY the provided evidence.

STRICT CITATION REQUIREMENTS:
- Every factual statement MUST contain a citation.
- Every citation MUST use one of these exact formats:
  [Text 1], [Text 2], [Chain 1], [Path 1], or [Metadata 1].
- Replace N with the actual evidence number.
- NEVER output [Text N], [Chain N], [Path N], or [Metadata N].
- NEVER use numeric citations such as [1], [2], or [3].
- NEVER invent citation numbers.
- Put the citation immediately after the claim it supports.
- If the evidence is insufficient, say so rather than guessing.

ANSWER RULES:
- Answer directly and concisely.
- Use only the supplied evidence.
- Prefer direct text evidence for factual questions.
- Use metadata for document-level facts such as authorship.
- Use reasoning chains for multi-hop reasoning.

Evidence:
{context}

Question:
{query}

Answer:
""".strip()