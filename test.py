from ingestion.loader import loader
from ingestion.cleaner import clean_text
from ingestion.chunker import TextChunker
text = loader.load("data/sample.txt")

text = clean_text(text)

chunker = TextChunker()
chunks = chunker.split(text)

print("Characters:", len(text))
print("Chunks:", len(chunks))

for chunk in chunks:
    print(f"\n--- Chunk {chunk.chunk_index} ---")
    print(chunk.content)