from generation.llm import llm_client
from generation.prompt import build_prompt
from retrieval.vector import retrieve


def answer_query(query: str, limit: int = 5) -> dict:
    results = retrieve(query, limit=limit)

    context_parts = []

    for result in results:
        context_parts.append(result.payload["content"])

    context = "\n\n".join(context_parts)

    prompt = build_prompt(
        query=query,
        context=context,
    )

    answer = llm_client.generate(prompt)

    sources = [
        {
            "source": result.payload.get("source"),
            "chunk_index": result.payload.get("chunk_index"),
            "score": result.score,
        }
        for result in results
    ]

    return {
        "answer": answer,
        "sources": sources,
    }