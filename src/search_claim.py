from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

client = QdrantClient(host="localhost", port=6333)
model = SentenceTransformer("all-MiniLM-L6-v2")

COLLECTION_NAME = "claims_memory"

query = "vaccines cause autism"
query_vector = model.encode(query).tolist()

# Use the newer query_points API; search is absent in some client versions.
response = client.query_points(
    collection_name=COLLECTION_NAME,
    query=query_vector,
    limit=1,
)

for point in response.points:
    print("Score:", point.score)
    print("Payload:", point.payload)
