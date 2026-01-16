from src.agents.retrieval_agent import RetrievalAgent

DEFAULT_VERDICT = "Unverified"


class VerdictAgent:
    def __init__(self):
        self.retriever = RetrievalAgent()

    def get_verdict(self, raw_claim: str):
        """
        Returns:
        - verdict (string)
        - explanation (string)
        """

        exists, payload, score = self.retriever.find_existing_claim(raw_claim)

        if exists:
            verdict = payload.get("verdict") or DEFAULT_VERDICT
            explanation = (
                f"This claim has been seen before. "
                f"Reusing stored verdict. "
                f"Seen count so far: {payload.get('seen_count')}."
            )
            return verdict, explanation

        # New claim
        return (
            DEFAULT_VERDICT,
            "This claim has not been seen before. "
            "Marked as Unverified until more evidence is available."
        )

from src.agents.verdict_agent import VerdictAgent

agent = VerdictAgent()

tests = [
    "Do vaccines cause autism?",
    "vaccines contain microchips"
]

for t in tests:
    verdict, explanation = agent.get_verdict(t)
    print("\nInput:", t)
    print("Verdict:", verdict)
    print("Explanation:", explanation)
