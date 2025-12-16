import json
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# Load SBERT model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Load your knowledge base file
with open("kb.json", "r", encoding="utf-8") as f:
    kb = json.load(f)

chunks = []
vectors = []

# Convert each KB item into chunks
for item in kb:
    text = item["content"]
    embedding = model.encode(text)

    chunks.append({
        "id": item["id"],
        "content": text
    })

    vectors.append(embedding)

# Save chunks
with open("chunks.json", "w", encoding="utf-8") as f:
    json.dump(chunks, f, indent=2)

# Build FAISS index
vectors_np = np.array(vectors).astype("float32")
index = faiss.IndexFlatL2(vectors_np.shape[1])
index.add(vectors_np)

faiss.write_index(index, "faiss.index")

print("Chunks + FAISS index generated successfully!")
