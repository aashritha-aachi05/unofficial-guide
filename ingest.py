"""Load Rutgers CS professor review .txt files, clean them, and chunk them.

Chunking strategy (see planning.md): fixed 300-character chunks with a
50-character overlap so an opinion that spans a chunk boundary isn't lost.
"""

import os
import re

DOCUMENTS_DIR = "documents"
CHUNK_SIZE = 300
CHUNK_OVERLAP = 50


def clean_text(text):
    """Collapse runs of whitespace (including newlines) into single spaces."""
    return re.sub(r"\s+", " ", text).strip()


def chunk_text(text, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    """Split text into overlapping fixed-size character chunks."""
    if not text:
        return []
    step = chunk_size - overlap
    chunks = []
    for start in range(0, len(text), step):
        chunk = text[start:start + chunk_size]
        chunks.append(chunk)
        if start + chunk_size >= len(text):
            break
    return chunks


def load_and_chunk(documents_dir=DOCUMENTS_DIR):
    """Load every .txt file in the folder and return a list of chunk records.

    Each record is a dict: {"source": <filename>, "text": <chunk>}.
    """
    records = []
    for filename in sorted(os.listdir(documents_dir)):
        if not filename.endswith(".txt"):
            continue
        path = os.path.join(documents_dir, filename)
        with open(path, "r", encoding="utf-8") as f:
            raw = f.read()
        cleaned = clean_text(raw)
        for chunk in chunk_text(cleaned):
            records.append({"source": filename, "text": chunk})
    return records


if __name__ == "__main__":
    records = load_and_chunk()
    print(f"Loaded {len(records)} chunks from '{DOCUMENTS_DIR}/'.\n")
    print("Sample chunks:\n")
    for i, record in enumerate(records[:5], start=1):
        print(f"--- Chunk {i} (source: {record['source']}) ---")
        print(record["text"])
        print()
