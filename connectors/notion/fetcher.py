from connectors.notion.client import NotionClient


class NotionFetcher:
    def __init__(self) -> None:
        self.client = NotionClient()

    def search(self, query: str = "", page_size: int = 10) -> list[dict]:
        payload = {"query": query, "page_size": page_size}
        data = self.client.post("/search", payload)
        results = data.get("results", [])

        while data.get("has_more"):
            payload["start_cursor"] = data["next_cursor"]
            data = self.client.post("/search", payload)
            results.extend(data.get("results", []))

        return results

    def query_database(self, database_id: str, page_size: int = 100) -> list[dict]:
        payload = {"page_size": page_size}
        data = self.client.post(f"/databases/{database_id}/query", payload)
        results = data.get("results", [])

        while data.get("has_more"):
            payload["start_cursor"] = data["next_cursor"]
            data = self.client.post(f"/databases/{database_id}/query", payload)
            results.extend(data.get("results", []))

        return results

    def get_block_children(self, block_id: str) -> list[dict]:
        params = {"page_size": 100}
        data = self.client.get(f"/blocks/{block_id}/children", params=params)
        results = data.get("results", [])

        while data.get("has_more"):
            params["start_cursor"] = data["next_cursor"]
            data = self.client.get(f"/blocks/{block_id}/children", params=params)
            results.extend(data.get("results", []))

        return results

    def get_all_blocks_recursive(self, block_id: str) -> list[dict]:
        all_blocks = []
        children = self.get_block_children(block_id)

        for child in children:
            all_blocks.append(child)
            if child.get("has_children"):
                all_blocks.extend(self.get_all_blocks_recursive(child["id"]))

        return all_blocks