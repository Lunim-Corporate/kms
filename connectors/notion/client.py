import requests

from core.config.settings import settings


class NotionClient:
    BASE_URL = "https://api.notion.com/v1"

    def __init__(self) -> None:
        if not settings.notion_api_key:
            raise ValueError("NOTION_API_KEY is missing in .env")

        self.headers = {
            "Authorization": f"Bearer {settings.notion_api_key}",
            "Notion-Version": settings.notion_version,
            "Content-Type": "application/json",
        }

    def post(self, path: str, payload: dict) -> dict:
        url = f"{self.BASE_URL}{path}"
        response = requests.post(url, headers=self.headers, json=payload, timeout=30)
        response.raise_for_status()
        return response.json()

    def get(self, path: str, params: dict | None = None) -> dict:
        url = f"{self.BASE_URL}{path}"
        response = requests.get(url, headers=self.headers, params=params, timeout=30)
        response.raise_for_status()
        return response.json()