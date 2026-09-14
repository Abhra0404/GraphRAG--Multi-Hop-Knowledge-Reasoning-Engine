from ingestion.chunker import TextChunker
from ingestion.cleaner import clean_text


def test_clean_text():
    text = "Hello    world\n\n\n\nGraphRAG"

    result = clean_text(text)

    assert result == "Hello world\n\nGraphRAG"


def test_chunker():
    text = "a" * 2500

    chunker = TextChunker(
        chunk_size=1000,
        overlap=100,
    )

    chunks = chunker.split(text)

    assert len(chunks) > 1
    assert chunks[0].chunk_index == 0
    assert chunks[1].chunk_index == 1


def test_empty_text():
    chunker = TextChunker()

    assert chunker.split("") == []