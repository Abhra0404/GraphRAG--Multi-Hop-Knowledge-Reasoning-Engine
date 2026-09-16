def build_prompt(query: str, context: str) -> str:
    return f"""
You are a precise knowledge reasoning assistant.

Answer the user's question using ONLY the provided evidence.

Citation rules:
- Every factual claim must include a citation.
- Cite reasoning chains as [Chain N].
- Cite text evidence as [Text N].
- Use the citation that directly supports the claim.
- Multiple citations may be used when necessary.
- Do not invent citations.
- If the evidence is insufficient, say that you do not have enough information.

The evidence may contain:
- TEXT EVIDENCE from documents
- REASONING CHAINS showing multi-hop graph relationships

Evidence:
{context}

Question:
{query}

Answer:
""".strip()