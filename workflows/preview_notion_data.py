from connectors.notion.fetcher import NotionFetcher


def get_plain_text(items: list[dict]) -> str:
    if not items:
        return ""
    return "".join(item.get("plain_text", "") for item in items)


def get_title(prop: dict) -> str:
    return get_plain_text(prop.get("title", []))


def get_select(prop: dict) -> str:
    value = prop.get("select")
    return value.get("name", "") if value else ""


def get_multi_select(prop: dict) -> list[str]:
    values = prop.get("multi_select", [])
    return [item.get("name", "") for item in values]


def get_files(prop: dict) -> list[dict]:
    files = prop.get("files", [])
    results = []

    for file in files:
        file_info = {
            "name": file.get("name", ""),
            "type": file.get("type", ""),
            "url": ""
        }

        if file.get("type") == "file":
            file_info["url"] = file.get("file", {}).get("url", "")

        elif file.get("type") == "external":
            file_info["url"] = file.get("external", {}).get("url", "")

        results.append(file_info)

    return results


def preview_row(row: dict) -> dict:
    props = row.get("properties", {})

    return {
        "id": row.get("id"),
        "title": get_title(props.get("Participant name", {})),
        "session": get_select(props.get("Session", {})),
        "category": get_multi_select(props.get("Category", {})),
        "created_time": row.get("created_time"),
        "updated_time": row.get("last_edited_time"),
        "files": get_files(props.get("Video", {})),
        "url": row.get("url"),
    }


def main() -> None:
    database_id = "31464be3-aa8c-8083-9671-c9090f324737"

    fetcher = NotionFetcher()
    rows = fetcher.query_database(database_id)

    print(f"\nTotal rows: {len(rows)}\n")

    for i, row in enumerate(rows[:10], start=1):
        clean = preview_row(row)

        print("=" * 80)
        print(f"Record {i}")
        print(f"ID: {clean['id']}")
        print(f"Title: {clean['title']}")
        print(f"Session: {clean['session']}")
        print(f"Category: {', '.join(clean['category']) if clean['category'] else 'None'}")
        print(f"Created: {clean['created_time']}")
        print(f"Updated: {clean['updated_time']}")
        print("Files:")
        if clean["files"]:
            for f in clean["files"]:
                print(f"  - {f['name']}")
                print(f"    URL: {f['url']}")
        else:
            print("  None")
        print(f"URL: {clean['url']}")
        print("=" * 80)


if __name__ == "__main__":
    main()