from graph.client import neo4j_client


class GraphRepository:
    def upsert_entity(
        self,
        name: str,
        entity_type: str,
        dataset: str,
        source_document: str | None = None,
        source_chunk: int | None = None,
    ) -> None:
        query = """
        MERGE (e:Entity {
            name: $name,
            dataset: $dataset
        })
        SET
            e.type = $entity_type,
            e.source_document = $source_document,
            e.source_chunk = $source_chunk
        """

        with neo4j_client.driver.session() as session:
            session.run(
                query,
                name=name,
                dataset=dataset,
                entity_type=entity_type,
                source_document=source_document,
                source_chunk=source_chunk,
            )

    def upsert_relation(
        self,
        source: str,
        relation: str,
        target: str,
        dataset: str,
        source_document: str | None = None,
        source_chunk: int | None = None,
    ) -> None:
        query = """
        MATCH (source:Entity {
            name: $source,
            dataset: $dataset
        })
        MATCH (target:Entity {
            name: $target,
            dataset: $dataset
        })
        MERGE (source)-[r:RELATED {
            type: $relation,
            dataset: $dataset
        }]->(target)
        SET
            r.source_document = $source_document,
            r.source_chunk = $source_chunk
        """

        with neo4j_client.driver.session() as session:
            session.run(
                query,
                source=source,
                relation=relation,
                target=target,
                dataset=dataset,
                source_document=source_document,
                source_chunk=source_chunk,
            )

    def get_entities(
        self,
        dataset: str | None = None,
    ) -> list[dict]:
        if dataset:
            query = """
            MATCH (e:Entity)
            WHERE e.dataset = $dataset
            RETURN
                e.name AS name,
                e.type AS type,
                e.dataset AS dataset,
                e.source_document AS source_document,
                e.source_chunk AS source_chunk
            ORDER BY e.name
            """
        else:
            query = """
            MATCH (e:Entity)
            RETURN
                e.name AS name,
                e.type AS type,
                e.dataset AS dataset,
                e.source_document AS source_document,
                e.source_chunk AS source_chunk
            ORDER BY e.name
            """

        with neo4j_client.driver.session() as session:
            result = session.run(
                query,
                dataset=dataset,
            )
            return [record.data() for record in result]


graph_repository = GraphRepository()