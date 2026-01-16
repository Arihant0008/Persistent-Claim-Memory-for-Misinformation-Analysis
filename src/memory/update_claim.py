import uuid
from datetime import datetime

from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

from src.normalize.normalize_claim import normalize_claim
from src.agents.retrieval_agent import RetrievalAgent

COLLECTION_NAME = "claims_memory"


class MemoryUpdater:
    def __init__(self):
        self.client = QdrantClient(host="localhost", port=6333)
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.retriever = RetrievalAgent()

    def process_claim(self, raw_claim: str):
        """
        Inserts or updates memory.
        Returns action taken and updated payload.
        """

        exists, payload, score = self.retriever.find_existing_claim(raw_claim)
        now = datetime.utcnow().isoformat()

        normalized = normalize_claim(raw_claim)
        vector = self.model.encode(normalized).tolist()

        if exists:
            # UPDATE existing claim
            new_count = payload["seen_count"] + 1

            self.client.upsert(
                collection_name=COLLECTION_NAME,
                points=[
                    {
                        "id": payload["id"],
                        "vector": vector,
                        "payload": {
                            **payload,
                            "seen_count": new_count,
                            "last_seen": now,
                        },
                    }
                ],
            )

            return "updated", {
                **payload,
                "seen_count": new_count,
                "last_seen": now,
            }

        # INSERT new claim
        point_id = str(uuid.uuid4())
        new_payload = {
            "normalized_claim": normalized,
            "verdict": "Unverified",
            "seen_count": 1,
            "first_seen": now,
            "last_seen": now,
        }

        self.client.upsert(
            collection_name=COLLECTION_NAME,
            points=[
                {
                    "id": point_id,
                    "vector": vector,
                    "payload": new_payload,
                }
            ],
        )

        return "inserted", new_payload
    
from src.memory.update_claim import MemoryUpdater

updater = MemoryUpdater()

claim = "Do vaccines cause autism?"

action1, payload1 = updater.process_claim(claim)
print(action1, payload1["seen_count"])

action2, payload2 = updater.process_claim(claim)
print(action2, payload2["seen_count"])
