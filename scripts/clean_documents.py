import json
import re
from pathlib import Path


def clean_text(text: str) -> str:
    if not text:
        return ""

    text = text.replace("\xa0", " ")
    text = text.replace("\t", " ")
    text = text.replace("\r", "\n")

    # collapse repeated spaces
    text = re.sub(r"[ ]{2,}", " ", text)

    # collapse 3+ newlines into 2
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


def main():
    input_path = Path("data/canonical_documents.json")
    output_path = Path("data/clean_documents.json")

    with open(input_path, "r", encoding="utf-8") as f:
        documents = json.load(f)

    cleaned_documents = []
    for doc in documents:
        cleaned_doc = {
            **doc,
            "content": clean_text(doc.get("content", "")),
        }
        cleaned_documents.append(cleaned_doc)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(cleaned_documents, f, indent=2, ensure_ascii=False)

    print(f"Cleaned {len(cleaned_documents)} documents")
    print(f"Saved to {output_path}")


if __name__ == "__main__":
    main()