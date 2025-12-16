# backend/rag_utils.py

import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

CHUNKS_FILE = "chunks.json"
FAISS_FILE = "faiss.index"

_model = None

def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model

def load_chunks():
    with open(CHUNKS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def load_index():
    return faiss.read_index(FAISS_FILE)

def search_kb(query, k=3):
    chunks = load_chunks()
    index = load_index()
    model = get_model()

    query_vec = model.encode([query]).astype("float32")
    distances, indices = index.search(query_vec, k)

    results = []
    for idx in indices[0]:
        if idx < len(chunks):
            results.append(chunks[idx]["content"])

    return results
