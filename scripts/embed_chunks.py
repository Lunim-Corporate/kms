import json
from pathlib import Path
from sentence_transformers import SentenceTransformer


def main():
    input_path = Path("data/chunks.json")
    output_path = Path("data/chunks_with_embeddings.json")

    with open(input_path, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    print(f"Loaded {len(chunks)} chunks")

    model = SentenceTransformer("all-MiniLM-L6-v2")
    print("Embedding model loaded")

    for i, chunk in enumerate(chunks, start=1):
        embedding = model.encode(chunk["text"]).tolist()
        chunk["embedding"] = embedding

        if i % 10 == 0:
            print(f"Embedded {i}/{len(chunks)} chunks")

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(chunks, f)

    print(f"Saved embedded chunks to {output_path}")


if __name__ == "__main__":
    main()