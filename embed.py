"""Embed review chunks and store them in ChromaDB for semantic retrieval.

Embedding model: all-MiniLM-L6-v2 (sentence-transformers), run locally.
Vector store: ChromaDB, persisted to disk so we don't re-embed every run.
See planning.md for the rationale.
"""

import chromadb
from chromadb.utils import embedding_functions

from ingest import load_and_chunk

CHROMA_DIR = "chroma_db"
COLLECTION_NAME = "professor_reviews"
EMBED_MODEL = "all-MiniLM-L6-v2"
TOP_K = 5

# all-MiniLM-L6-v2 is used for BOTH ingestion and query embedding, so chunks
# and questions land in the same vector space.
_embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name=EMBED_MODEL
)


def _client():
    return chromadb.PersistentClient(path=CHROMA_DIR)


def get_collection():
    """Return the reviews collection (created if it doesn't exist)."""
    return _client().get_or_create_collection(
        name=COLLECTION_NAME,
        embedding_function=_embedding_fn,
    )


def build_index():
    """(Re)build the vector store from the documents folder.

    Drops any existing collection first so repeated runs don't pile up
    duplicate chunks.
    """
    client = _client()
    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass  # collection didn't exist yet — fine on a first run

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        embedding_function=_embedding_fn,
    )

    records = load_and_chunk()
    collection.add(
        ids=[f"chunk-{i}" for i in range(len(records))],
        documents=[r["text"] for r in records],
        metadatas=[{"source": r["source"]} for r in records],
    )
    return collection


def ensure_index():
    """Build the index if it's empty (e.g. a fresh deploy with no chroma_db).

    Lets the app boot on a hosting platform where the local vector store
    doesn't exist yet, without forcing a manual `python embed.py` run.
    """
    collection = get_collection()
    if collection.count() == 0:
        return build_index()
    return collection


def retrieve(query, k=TOP_K):
    """Return the top-k chunks most similar to `query`.

    Each result is a dict: {"text", "source", "distance"} where a smaller
    distance means a closer (more relevant) match.
    """
    collection = get_collection()
    results = collection.query(query_texts=[query], n_results=k)
    out = []
    for text, meta, distance in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0],
    ):
        out.append(
            {"text": text, "source": meta["source"], "distance": distance}
        )
    return out


if __name__ == "__main__":
    collection = build_index()
    print(f"Indexed {collection.count()} chunks into '{COLLECTION_NAME}'.\n")

    sample_query = "What do students say about Sesh Venugopal's exams?"
    print(f"Sample query: {sample_query}\n")
    for i, hit in enumerate(retrieve(sample_query), start=1):
        print(f"--- Result {i} (source: {hit['source']}, distance: {hit['distance']:.3f}) ---")
        print(hit["text"])
        print()
