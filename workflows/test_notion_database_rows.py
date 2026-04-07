from pprint import pprint

from connectors.notion.fetcher import NotionFetcher


def main() -> None:
    database_id = "3277f0e2-e999-8044-a8b0-e803ee58adb2"

    fetcher = NotionFetcher()
    rows = fetcher.query_database(database_id)

    print(f"Rows found: {len(rows)}\n")

    if rows:
        pprint(rows[0])
    else:
        print("No rows found.")


if __name__ == "__main__":
    main()