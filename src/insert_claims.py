import json
import uuid
from datetime import datetime
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

client = QdrantClient(host="localhost", port=6333)
model = SentenceTransformer("all-MiniLM-L6-v2")

COLLECTION_NAME = "claims_memory"

with open("data/dummy_client.json") as f:
    claims = json.load(f)

vectors = model.encode(claims)

points = []
now = datetime.utcnow().isoformat()

for claim, vector in zip(claims, vectors):
    points.append({
        "id": str(uuid.uuid4()),
        "vector": vector.tolist(),
        "payload": {
            "normalized_claim": claim,
            "verdict": None,
            "seen_count": 1,
            "first_seen": now,
            "last_seen": now
        }
    })

client.upsert(collection_name=COLLECTION_NAME, points=points)

print("Inserted claims into memory")
