from generation.llm import llm_client
from generation.prompt import build_prompt
from reasoning.chain import build_reasoning_chains
from reasoning.evidence import build_evidence
from reasoning.fusion import fuse_evidence
from reasoning.reasoner import build_valid_reasoning_chains
from retrieval.hybrid import hybrid_retrieve


def answer_query(query: str) -> dict:
    retrieval_results = hybrid_retrieve(query)

    reasoning_chains = build_reasoning_chains(
        retrieval_results["graph"]
    )

    reasoning_chains = build_valid_reasoning_chains(
        reasoning_chains,
        retrieval_results["plan"]["entities"],
        retrieval_results["plan"][
            "relationship_types"
        ],
    )

    evidence_bundle = fuse_evidence(
        text_evidence=retrieval_results["vector"],
        reasoning_chains=reasoning_chains,
    )

    evidence = build_evidence(
        text_evidence=evidence_bundle.text,
        graph_results=retrieval_results["graph"],
        reasoning_chains=evidence_bundle.chains,
        metadata=retrieval_results["metadata"],
    )

    prompt = build_prompt(
        query=query,
        context=evidence,
    )

    answer = llm_client.generate(prompt)

    return {
        "answer": answer,
        "entities": retrieval_results["plan"]["entities"],
        "reasoning_chains": reasoning_chains,
        "evidence": evidence,
    }