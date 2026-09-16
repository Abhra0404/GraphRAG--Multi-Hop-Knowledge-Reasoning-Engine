from graph.client import neo4j_client


def retrieve_graph(
    entity_name: str,
    hops: int = 2,
    limit: int = 20,
) -> list[dict]:
    query = f"""
    MATCH (start:Entity)
    WHERE toLower(start.name) CONTAINS toLower($entity_name)

    MATCH path = (start)-[*1..{hops}]->(related:Entity)

    RETURN
        [node IN nodes(path) | node.name] AS nodes,
        [rel IN relationships(path) | rel.type] AS relationships,
        [rel IN relationships(path) | rel.source_document] AS sources,
        [rel IN relationships(path) | rel.source_chunk] AS chunks

    LIMIT $limit
    """

    with neo4j_client.driver.session() as session:
        result = session.run(
            query,
            entity_name=entity_name,
            limit=limit,
        )

        paths = []

        for record in result:
            paths.append(
                {
                    "nodes": record["nodes"],
                    "relationships": record["relationships"],
                    "sources": record["sources"],
                    "chunks": record["chunks"],
                }
            )

        return paths