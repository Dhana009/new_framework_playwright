from api.api_client import APIClient


class AdminSeed:
    def __init__(self, api_client: APIClient):
        self.api_client = api_client

    def ensure(self):
        if self._seed_exists():
            return
        self._create_seed()

    def _seed_exists(self) -> bool:
        response = self.api_client.get("/items?limit=1")
        response.raise_for_status()
        total = response.json().get("pagination", {}).get("total", 0)
        return total > 0

    def _create_seed(self):
        payload = {
            "name": "Test Item",
            "description": (
                "This is a test item description that meets "
                "the minimum length requirement of 10 characters."
            ),
            "item_type": "DIGITAL",
            "price": 10.00,
            "category": "Software",
            "download_url": "https://example.com/file.zip",
            "file_size": 1024,
        }
        response = self.api_client.post("/items", json=payload)
        response.raise_for_status()
