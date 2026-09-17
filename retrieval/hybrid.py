from reasoning.entity_linker import link_entities
from reasoning.fusion_ranker import rank_fused_evidence
from reasoning.path_ranker import rank_paths
from reasoning.planner import plan_query
from retrieval.graph import retrieve_graph
from retrieval.vector import retrieve
from reasoning.conflict import detect_conflicts

def hybrid_retrieve(
    query: str,
    vector_limit: int = 5,
    graph_limit: int = 5,
) -> dict:
    plan = plan_query(query)

    linked_entities = link_entities(
        plan["entities"]
    )

    plan["entities"] = linked_entities

    vector_results = retrieve(
        query,
        limit=vector_limit,
    )

    graph_results = []

    for entity in linked_entities:
        graph_results.extend(
            retrieve_graph(
                entity,
                hops=plan["max_hops"],
            )
        )

    ranked_graph_results = rank_paths(
        paths=graph_results,
        query_entities=linked_entities,
        limit=graph_limit,
        
    )

    conflicts = detect_conflicts(
        vector_results,
        ranked_graph_results,
    )

    fused_evidence = rank_fused_evidence(
        vector_results=vector_results,
        graph_results=ranked_graph_results,
    )

    return {
        "plan": plan,
        "vector": vector_results,
        "graph": ranked_graph_results,
        "fused": fused_evidence,
        "conflicts": conflicts,
    }