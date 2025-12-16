import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Files
CHUNKS_FILE = "chunks.json"
FAISS_FILE = "faiss.index"

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Load chunks
with open(CHUNKS_FILE, "r", encoding="utf-8") as f:
    chunks = json.load(f)

texts = [chunk["content"] for chunk in chunks]

# Create embeddings
embeddings = model.encode(texts, show_progress_bar=True)
embeddings = np.array(embeddings).astype("float32")

# Build FAISS index
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

# Save index
faiss.write_index(index, FAISS_FILE)

print(" FAISS index rebuilt successfully from chunk['content']")
print(f"Total vectors indexed: {index.ntotal}")
