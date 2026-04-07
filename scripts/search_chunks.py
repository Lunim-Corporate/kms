import json
from pathlib import Path
from sentence_transformers import SentenceTransformer
import numpy as np


def cosine_similarity(a, b):
    a = np.array(a)
    b = np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def main():
    input_path = Path("data/chunks_with_embeddings.json")

    with open(input_path, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    model = SentenceTransformer("all-MiniLM-L6-v2")

    query = input("Enter your query: ").strip()
    query_embedding = model.encode(query).tolist()

    scored_chunks = []
    for chunk in chunks:
        score = cosine_similarity(query_embedding, chunk["embedding"])
        scored_chunks.append((score, chunk))

    scored_chunks.sort(key=lambda x: x[0], reverse=True)

    top_k = 5
    print(f"\nTop {top_k} results for: {query}\n")

    for i, (score, chunk) in enumerate(scored_chunks[:top_k], start=1):
        print("=" * 100)
        print(f"Rank: {i}")
        print(f"Score: {score:.4f}")
        print(f"Title: {chunk['title']}")
        print(f"Session: {chunk['metadata'].get('session')}")
        print(f"Category: {chunk['metadata'].get('category')}")
        print(f"Text:\n{chunk['text']}")
        print("=" * 100)
        print()


if __name__ == "__main__":
    main()