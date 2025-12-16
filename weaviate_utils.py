import weaviate
from sentence_transformers import SentenceTransformer

client = weaviate.Client("http://localhost:8080")

model = SentenceTransformer("all-MiniLM-L6-v2")

CLASS_NAME = "DBSChunk"

def search_weaviate(query, k=3):
    query_vec = model.encode(query).tolist()

    result = (
        client.query
        .get(CLASS_NAME, ["content"])
        .with_near_vector({"vector": query_vec})
        .with_limit(k)
        .do()
    )

    chunks = result["data"]["Get"].get(CLASS_NAME, [])
    return [c["content"] for c in chunks]
