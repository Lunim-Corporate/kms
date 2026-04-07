from connectors.notion.fetcher import NotionFetcher
from connectors.notion.page_parser import blocks_to_text


def get_title(row: dict) -> str:
    title_prop = row.get("properties", {}).get("Participant name", {})
    return "".join(item.get("plain_text", "") for item in title_prop.get("title", []))


def get_files(row: dict) -> list[dict]:
    files_prop = row.get("properties", {}).get("Video&files", {})
    files = files_prop.get("files", [])

    result = []
    for f in files:
        url = f.get("file", {}).get("url") or f.get("external", {}).get("url") or ""
        name = f.get("name", "")

        if name.startswith("http") and url:
            clean_part = url.split("?")[0]
            name = clean_part.rstrip("/").split("/")[-1]

        result.append({
            "name": name,
            "url": url
        })

    return result


def get_select(row: dict, field_name: str) -> str:
    prop = row.get("properties", {}).get(field_name, {})
    value = prop.get("select")
    return value.get("name", "") if value else ""


def get_multi_select(row: dict, field_name: str) -> list[str]:
    prop = row.get("properties", {}).get(field_name, {})
    return [item.get("name", "") for item in prop.get("multi_select", [])]

def assess_content_quality(content: str) -> dict:
    if not content or not content.strip():
        return {
            "has_meaningful_content": False,
            "is_template_like": True,
            "content_length": 0,
        }

    template_markers = [
        "Context, objectives, and scope of the document",
        "Research findings, data insights, and key considerations",
        "Proposed solutions, strategies, and next steps",
        "Action items, timeline, and resource requirements",
    ]

    marker_hits = sum(1 for marker in template_markers if marker in content)
    content_length = len(content.strip())

    is_template_like = marker_hits >= 2
    has_meaningful_content = content_length > 300 and not is_template_like

    return {
        "has_meaningful_content": has_meaningful_content,
        "is_template_like": is_template_like,
        "content_length": content_length,
    }

def build_document(row, fetcher):
    page_id = row["id"]

    # page content
    blocks = fetcher.get_all_blocks_recursive(page_id)
    content = blocks_to_text(blocks)
    content_quality = assess_content_quality(content)

    return {
    "id": page_id,
    "title": get_title(row),
    "content": content,
    "files": get_files(row),
    "metadata": {
        "created_time": row.get("created_time"),
        "last_edited_time": row.get("last_edited_time"),
        "session": get_select(row, "Session"),
        "category": get_multi_select(row, "Category"),
        "has_meaningful_content": content_quality["has_meaningful_content"],
        "is_template_like": content_quality["is_template_like"],
        "content_length": content_quality["content_length"],
    }
}


def main():
    import json
    from pathlib import Path

    database_id = "31464be3-aa8c-8083-9671-c9090f324737"

    fetcher = NotionFetcher()
    rows = fetcher.query_database(database_id)

    documents = [build_document(row, fetcher) for row in rows]

    Path("data").mkdir(exist_ok=True)

    with open("data/canonical_documents.json", "w", encoding="utf-8") as f:
        json.dump(documents, f, indent=2, ensure_ascii=False)

    print(f"Built {len(documents)} documents")
    print("Saved to data/canonical_documents.json\n")

    for doc in documents[:2]:
        print(doc)
        print("=" * 80)

if __name__ == "__main__":
    main()