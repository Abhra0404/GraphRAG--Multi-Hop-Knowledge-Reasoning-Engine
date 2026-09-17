from pydantic import BaseModel, Field


class TextEvidence(BaseModel):
    content: str
    source: str
    chunk_index: int | None = None
    score: float = 0.0


class ReasoningStep(BaseModel):
    relationship: str
    target: str
    source_document: str | None = None
    source_chunk: int | None = None


class ReasoningChain(BaseModel):
    start: str
    steps: list[ReasoningStep] = Field(
        default_factory=list
    )
    score: float = 0.0
    confidence: float = 0.0

class EvidenceConflict(BaseModel):
    type: str
    source: str
    relationship: str
    graph_target: str
    text: str

class EvidenceBundle(BaseModel):
    text: list[TextEvidence] = Field(
        default_factory=list
    )
    chains: list[ReasoningChain] = Field(
        default_factory=list
    )
    conflicts: list[EvidenceConflict] = Field(
        default_factory=list
    )