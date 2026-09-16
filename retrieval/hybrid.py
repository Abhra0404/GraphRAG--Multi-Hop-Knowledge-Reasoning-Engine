from reasoning.path_ranker import rank_paths
from reasoning.planner import plan_query
from retrieval.graph import retrieve_graph
from retrieval.vector import retrieve


def hybrid_retrieve(
    query: str,
    vector_limit: int = 5,
    graph_limit: int = 5,
) -> dict:
    plan = plan_query(query)

    vector_results = retrieve(
        query,
        limit=vector_limit,
    )

    graph_results = []

    for entity in plan["entities"]:
        graph_results.extend(
            retrieve_graph(
                entity,
                hops=plan["max_hops"],
            )
        )

    ranked_graph_results = rank_paths(
        paths=graph_results,
        query_entities=plan["entities"],
        limit=graph_limit,
    )

    return {
        "plan": plan,
        "vector": vector_results,
        "graph": ranked_graph_results,
    }