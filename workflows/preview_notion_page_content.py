from connectors.notion.fetcher import NotionFetcher
from connectors.notion.page_parser import blocks_to_text


def get_title(row: dict) -> str:
    title_prop = row.get("properties", {}).get("Participant name", {})
    return "".join(item.get("plain_text", "") for item in title_prop.get("title", []))


def main() -> None:
    database_id = "31464be3-aa8c-8083-9671-c9090f324737"

    fetcher = NotionFetcher()
    rows = fetcher.query_database(database_id)

    print(f"Total rows: {len(rows)}\n")

    for i, row in enumerate(rows[:5], start=1):
        page_id = row["id"]
        title = get_title(row)

        blocks = fetcher.get_all_blocks_recursive(page_id)
        content = blocks_to_text(blocks)

        print("=" * 80)
        print(f"Record {i}")
        print(f"Title: {title}")
        print(f"Page ID: {page_id}")
        print("Written content on page:")
        print(content if content else "[No text written directly on this Notion page]")
        print("=" * 80)
        print()


if __name__ == "__main__":
    main()