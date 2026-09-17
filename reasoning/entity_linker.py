from graph.client import neo4j_client


def link_entity(entity: str) -> str | None:
    query = """
    MATCH (e:Entity)
    WHERE toLower(e.name) = toLower($entity)
       OR toLower(e.name) CONTAINS toLower($entity)
       OR toLower($entity) CONTAINS toLower(e.name)
    RETURN e.name AS name
    LIMIT 1
    """

    with neo4j_client.driver.session() as session:
        result = session.run(
            query,
            entity=entity,
        )

        record = result.single()

        if record:
            return record["name"]

    return None


def link_entities(entities: list[str]) -> list[str]:
    linked = []

    for entity in entities:
        canonical = link_entity(entity)

        if canonical and canonical not in linked:
            linked.append(canonical)

    return linked