import json
import weaviate
from sentence_transformers import SentenceTransformer

client = weaviate.Client("http://localhost:8080")
model = SentenceTransformer("all-MiniLM-L6-v2")

CLASS_NAME = "DBSChunk"

# Create schema
if not client.schema.contains({"class": CLASS_NAME}):
    client.schema.create_class({
        "class": CLASS_NAME,
        "vectorizer": "none",
        "properties": [
            {"name": "content", "dataType": ["text"]}
        ]
    })

# Load chunks
with open("chunks.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)

for chunk in chunks:
    embedding = model.encode(chunk["content"]).tolist()
    client.data_object.create(
        data_object={"content": chunk["content"]},
        class_name=CLASS_NAME,
        vector=embedding
    )

print("Data ingested into Weaviate")
