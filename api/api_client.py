import requests


class APIClient:
    """
    Stateless API client for seed operations.
    """

    def __init__(self, base_url: str, token: str):
        self.base_url = base_url.rstrip("/")
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

    def get(self, path: str):
        return requests.get(
            f"{self.base_url}{path}",
            headers=self.headers,
            timeout=10,
        )

    def post(self, path: str, json: dict):
        return requests.post(
            f"{self.base_url}{path}",
            headers=self.headers,
            json=json,
            timeout=10,
        )
