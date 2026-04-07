import json
from pathlib import Path


def chunk_text(text: str, chunk_size: int = 800, overlap: int = 150) -> list[str]:
    if not text:
        return []

    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = start + chunk_size
        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        if end >= text_length:
            break

        start += chunk_size - overlap

    return chunks


def main():
    input_path = Path("data/clean_documents.json")
    output_path = Path("data/chunks.json")

    with open(input_path, "r", encoding="utf-8") as f:
        documents = json.load(f)

    all_chunks = []

    for doc in documents:
        doc_chunks = chunk_text(doc.get("content", ""))

        for i, chunk in enumerate(doc_chunks):
            all_chunks.append({
                "chunk_id": f"{doc['id']}_{i}",
                "doc_id": doc["id"],
                "title": doc["title"],
                "text": chunk,
                "metadata": doc["metadata"],
                "files": doc.get("files", []),
            })

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, indent=2, ensure_ascii=False)

    print(f"Created {len(all_chunks)} chunks")
    print(f"Saved to {output_path}")


if __name__ == "__main__":
    main()