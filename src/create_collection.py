from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance

client = QdrantClient(host="localhost", port=6333)

COLLECTION_NAME = "claims_memory"
VECTOR_SIZE = 384  # must match embedding model

# Create the collection if missing; otherwise leave it as-is.
if not client.collection_exists(COLLECTION_NAME):
    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(size=VECTOR_SIZE, distance=Distance.COSINE),
    )
    print("Collection created:", COLLECTION_NAME)
else:
    print("Collection already exists:", COLLECTION_NAME)
