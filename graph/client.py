from neo4j import Driver, GraphDatabase

from core.config import settings


class Neo4jClient:
    def __init__(self):
        self.driver: Driver = GraphDatabase.driver(
            settings.neo4j_uri,
            auth=(
                settings.neo4j_user,
                settings.neo4j_password,
            ),
        )

    def verify_connection(self) -> bool:
        try:
            self.driver.verify_connectivity()
            return True
        except Exception:
            return False

    def close(self):
        self.driver.close()


neo4j_client = Neo4jClient()