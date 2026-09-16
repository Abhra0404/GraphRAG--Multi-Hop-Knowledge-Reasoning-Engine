def build_prompt(query: str, context: str) -> str:
    return f"""
You are a precise question-answering assistant.

Answer the user's question using only the provided context.

If the context does not contain enough information to answer,
say that you do not have enough information.

Context:
{context}

Question:
{query}

Answer:
""".strip()