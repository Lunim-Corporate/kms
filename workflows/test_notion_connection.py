from pprint import pprint

from connectors.notion.client import NotionClient


def main() -> None:
    client = NotionClient()
    data = client.post("/search", {"page_size": 10})

    print("Connected to Notion successfully.")
    print(f"Results found: {len(data.get('results', []))}")
    print("\nFirst result preview:\n")

    results = data.get("results", [])
    if results:
        pprint(results[0])
    else:
        print("No pages found. Make sure your page/database is shared with the integration.")


if __name__ == "__main__":
    main()
    