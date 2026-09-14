from dataclasses import dataclass


@dataclass
class TextChunk:
    content: str
    chunk_index: int


class TextChunker:
    def __init__(
        self,
        chunk_size: int = 1000,
        overlap: int = 150,
    ):
        if overlap >= chunk_size:
            raise ValueError(
                "overlap must be smaller than chunk_size"
            )

        self.chunk_size = chunk_size
        self.overlap = overlap

    def split(self, text: str) -> list[TextChunk]:
        if not text.strip():
            return []

        chunks = []

        start = 0
        index = 0

        while start < len(text):
            end = start + self.chunk_size

            chunk = text[start:end].strip()

            if chunk:
                chunks.append(
                    TextChunk(
                        content=chunk,
                        chunk_index=index,
                    )
                )

                index += 1

            if end >= len(text):
                break

            start = end - self.overlap

        return chunks