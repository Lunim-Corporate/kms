from pprint import pprint

from connectors.notion.fetcher import NotionFetcher
from connectors.notion.mapper import map_database_row_to_document


def main() -> None:
    database_id = "3277f0e2-e999-8044-a8b0-e803ee58adb2"

    fetcher = NotionFetcher()
    rows = fetcher.query_database(database_id)

    documents = [map_database_row_to_document(row) for row in rows]

    print(f"Mapped documents: {len(documents)}\n")

    for doc in documents[:3]:
        pprint(doc)
        print("-" * 80)


if __name__ == "__main__":
    main()