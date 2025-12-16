# backend/rag_utils.py

import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

CHUNKS_FILE = "chunks.json"
FAISS_FILE = "faiss.index"

# ------------------------------
# Lazy-loaded global objects
# ------------------------------
_model = None
_index = None
_chunks = None


def get_model():
    """Load embedding model only once"""
    global _model
    if _model is None:
        print("Loading SentenceTransformer model...")
        _model = SentenceTransformer("all-MiniLM-L6-v2")
        print("Embedding model loaded")
    return _model


def load_chunks():
    """Load chunk text once"""
    global _chunks
    if _chunks is None:
        with open(CHUNKS_FILE, "r", encoding="utf-8") as f:
            _chunks = json.load(f)
        print(f"Loaded {len(_chunks)} chunks")
    return _chunks


def load_index():
    """Load FAISS index once"""
    global _index
    if _index is None:
        _index = faiss.read_index(FAISS_FILE)
        print("FAISS index loaded")
    return _index


def search_kb(query: str, k: int = 3):
    """
    Perform vector similarity search
    """
    model = get_model()
    chunks = load_chunks()
    index = load_index()

    # Encode query
    query_vec = model.encode([query]).astype("float32")

    # Vector search
    distances, indices = index.search(query_vec, k)

    results = []
    for idx in indices[0]:
        if 0 <= idx < len(chunks):
            results.append(chunks[idx]["content"])

    return results
