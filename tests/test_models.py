from core.models import (
    Chunk,
    Document,
    DocumentStatus,
    IngestionJob,
    JobStatus,
)


def test_document_model():
    document = Document(
        filename="paper.pdf",
        content_type="application/pdf",
        file_path="/data/paper.pdf",
        status=DocumentStatus.PENDING,
    )

    assert document.filename == "paper.pdf"
    assert document.status == DocumentStatus.PENDING


def test_chunk_model():
    chunk = Chunk(
        content="GraphRAG combines graph retrieval with RAG.",
        chunk_index=0,
        metadata_={"page": 1},
    )

    assert chunk.chunk_index == 0
    assert chunk.metadata_["page"] == 1


def test_ingestion_job_model():
    job = IngestionJob(
        status=JobStatus.PENDING,
    )

    assert job.status == JobStatus.PENDING