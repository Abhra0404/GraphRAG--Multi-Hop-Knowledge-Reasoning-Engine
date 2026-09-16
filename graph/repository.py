from graph.client import neo4j_client


class GraphRepository:
    def upsert_entity(self, name: str, entity_type: str) -> None:
        query = """
        MERGE (e:Entity {name: $name})
        SET e.type = $entity_type
        """

        with neo4j_client.driver.session() as session:
            session.run(
                query,
                name=name,
                entity_type=entity_type,
            )

    def upsert_relation(
        self,
        source: str,
        relation: str,
        target: str,
        source_document: str | None = None,
        source_chunk: int | None = None,
    ) -> None:
        query = """
        MATCH (source:Entity {name: $source})
        MATCH (target:Entity {name: $target})

        MERGE (source)-[r:RELATED {type: $relation}]->(target)

        SET
            r.source_document = $source_document,
            r.source_chunk = $source_chunk
        """

        with neo4j_client.driver.session() as session:
            session.run(
                query,
                source=source,
                target=target,
                relation=relation,
                source_document=source_document,
                source_chunk=source_chunk,
            )

    def get_entities(self) -> list[dict]:
        query = """
        MATCH (e:Entity)
        RETURN e.name AS name, e.type AS type
        ORDER BY e.name
        """

        with neo4j_client.driver.session() as session:
            result = session.run(query)
            return [record.data() for record in result]


graph_repository = GraphRepository()