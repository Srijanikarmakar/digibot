# utils.py
import json
import os
import numpy as np
from sentence_transformers import SentenceTransformer

# Optional: try to import FAISS; if not available, we will fallback to numpy search
USE_FAISS = True
try:
    import faiss
except Exception:
    faiss = None
    USE_FAISS = False

KB_PATH = "kb.json"
EMBED_MODEL_NAME = "all-MiniLM-L6-v2"  # compact, fast, good for RAG

# Load model once
_model = SentenceTransformer(EMBED_MODEL_NAME)

# Global containers
_KB = []
_kb_embeddings = None
_faiss_index = None
_dim = None

def _load_kb():
    global _KB
    if _KB:
        return _KB
    with open(KB_PATH, "r", encoding="utf-8") as f:
        _KB = json.load(f)
    return _KB

def build_index():
    """
    Build embeddings for KB and create a FAISS index (or keep numpy arrays for fallback).
    This runs at import time (or call explicitly).
    """
    global _kb_embeddings, _faiss_index, _dim
    kb = _load_kb()
    texts = [item["content"] for item in kb]
    # generate embeddings (numpy array, shape = (n, dim))
    emb = _model.encode(texts, convert_to_numpy=True, show_progress_bar=True)
    # normalize to unit vectors (cosine similarity via inner product)
    norms = np.linalg.norm(emb, axis=1, keepdims=True)
    norms[norms == 0] = 1e-9
    emb = emb / norms

    _kb_embeddings = emb
    _dim = emb.shape[1]

    if USE_FAISS and faiss is not None:
        # Build FAISS index (IndexFlatIP for inner product on normalized vectors -> cosine)
        index = faiss.IndexFlatIP(_dim)
        index.add(emb.astype("float32"))
        _faiss_index = index
        print(f"[utils] Built FAISS index with {emb.shape[0]} vectors (dim={_dim})")
    else:
        _faiss_index = None
        print(f"[utils] FAISS not available — falling back to NumPy brute-force search with {emb.shape[0]} vectors")

# Ensure index built at import time
build_index()

def embed_text(text):
    """
    Return a normalized vector (numpy array) for the given text.
    """
    v = _model.encode([text], convert_to_numpy=True)[0]
    norm = np.linalg.norm(v)
    if norm == 0:
        return v
    return v / norm

def search_kb(vector, top_k=4):
    """
    Return a list of matches: [{"id":..., "title":..., "content":..., "score": ...}, ...]
    Scores are cosine similarities (0..1).
    """
    kb = _load_kb()
    if _faiss_index is not None:
        # FAISS expects float32 and 2D array
        q = np.array([vector]).astype("float32")
        D, I = _faiss_index.search(q, top_k)  # D: similarities, I: indices
        results = []
        for score, idx in zip(D[0], I[0]):
            if idx < 0 or idx >= len(kb):
                continue
            results.append({
                "id": kb[idx]["id"],
                "title": kb[idx].get("title"),
                "content": kb[idx]["content"],
                "score": float(score)
            })
        return results
    else:
        # NumPy fallback (cosine via dot of normalized vectors)
        emb = _kb_embeddings  # (n, dim)
        q = vector / (np.linalg.norm(vector) + 1e-9)
        sims = (emb @ q).astype(float)  # (n,)
        idxs = np.argsort(-sims)[:top_k]
        results = []
        for idx in idxs:
            results.append({
                "id": kb[idx]["id"],
                "title": kb[idx].get("title"),
                "content": kb[idx]["content"],
                "score": float(sims[idx])
            })
        return results
