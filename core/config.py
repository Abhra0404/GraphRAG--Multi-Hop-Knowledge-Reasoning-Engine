from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "GraphRAG"
    environment: str = "development"
    debug: bool = True

    postgres_url: str = "postgresql+psycopg://graphrag:graphrag@localhost:5432/graphrag"

    neo4j_uri: str = "bolt://localhost:7687"
    neo4j_user: str = "neo4j"
    neo4j_password: str = "password"

    qdrant_url: str = "http://localhost:6333"

    redis_url: str = "redis://localhost:6379/0"

    groq_api_key: str = ""
    llm_model: str = "openai/gpt-oss-20b"
    model_name: str = "gpt-5.6"
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()