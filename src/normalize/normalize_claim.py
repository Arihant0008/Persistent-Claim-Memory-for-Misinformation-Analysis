import re

STOPWORDS = {
    "do", "does", "did",
    "is", "are", "was", "were",
    "can", "could", "will", "would", "should",
    "a", "an", "the",  # articles
    "in", "on", "at", "to", "from", "by"  # prepositions
}

def normalize_claim(text: str) -> str:
    """
    Deterministically normalize a claim string.
    This function MUST NEVER change after Day 2.
    """

    # 1. lowercase
    text = text.lower()

    # 2. remove punctuation
    text = re.sub(r"[^a-z0-9\s]", "", text)

    # 3. collapse multiple spaces
    text = re.sub(r"\s+", " ", text).strip()

    # 4. remove simple stopwords
    words = text.split()
    words = [w for w in words if w not in STOPWORDS]

    return " ".join(words)


if __name__ == "__main__":
    tests = [
        "Do vaccines cause autism?",
        "vaccines cause autism",
        "Vaccines, cause autism!"
    ]

    for t in tests:
        print(normalize_claim(t))
