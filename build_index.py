# backend/build_index.py

import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

MODEL_NAME = "all-MiniLM-L6-v2"
model = SentenceTransformer(MODEL_NAME)

# Read manual.txt
with open("manual.txt", "r", encoding="utf-8") as f:
    lines = [line.strip() for line in f if line.strip()]

chunks = []
embeddings = []

for i, text in enumerate(lines):
    chunks.append({"id": i, "content": text})
    embeddings.append(model.encode(text))

# Save chunks
with open("chunks.json", "w", encoding="utf-8") as f:
    json.dump(chunks, f, indent=2)

# Build FAISS index
vectors = np.array(embeddings).astype("float32")
index = faiss.IndexFlatL2(vectors.shape[1])
index.add(vectors)

faiss.write_index(index, "faiss.index")

print("chunks.json and faiss.index created successfully")
