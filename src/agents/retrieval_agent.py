from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

from src.normalize.normalize_claim import normalize_claim

COLLECTION_NAME = "claims_memory"
SIMILARITY_THRESHOLD = 0.85


class RetrievalAgent:
    def __init__(self):
        self.client = QdrantClient(host="localhost", port=6333)
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def find_existing_claim(self, raw_claim: str):
        """
        Returns:
        - (True, payload, score) if claim exists
        - (False, None, score) if claim is new
        """

        # 1. Normalize
        normalized = normalize_claim(raw_claim)

        # 2. Embed normalized claim
        vector = self.model.encode(normalized).tolist()

        # 3. Query Qdrant
        response = self.client.query_points(
            collection_name=COLLECTION_NAME,
            query=vector,
            limit=1,
        )

        # 4. No memory yet
        if not response.points:
            return False, None, None

        top = response.points[0]

        # 5. Similarity decision
        # Include the point ID in the payload
        if top.score >= SIMILARITY_THRESHOLD:
            return True, {"id": top.id, **top.payload}, top.score

        return False, None, top.score

from src.agents.retrieval_agent import RetrievalAgent

agent = RetrievalAgent()

tests = [
    "Do vaccines cause autism?",
    "vaccines cause autism",
    "Is the earth flat?"
]

for t in tests:
    exists, payload, score = agent.find_existing_claim(t)
    print(f"\nInput: {t}")
    print("Exists:", exists)
    print("Score:", score)
    print("Payload:", payload)
