from pydantic import BaseModel, Field


class QueryRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=1,
        max_length=2000,
        description="Question to answer using the GraphRAG pipeline.",
    )


class QueryResponse(BaseModel):
    answer: str
    entities: list[str]
    evidence: str