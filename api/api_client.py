import requests


class APIClient:
    """
    Stateless API client for backend operations (seed data).

    Responsibilities:
    - Attach Authorization: Bearer <token>
    - Perform GET / POST requests
    - No internal auth mutation
    - Safe for session-level reuse
    """

    def __init__(self, backend_base_url: str, access_token: str):
        self.base_url = backend_base_url.rstrip("/")
        self.headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }

    def get(self, path: str):
        """
        Perform GET request.

        Example:
        client.get("/items")
        """
        return requests.get(
            f"{self.base_url}{path}",
            headers=self.headers,
        )

    def post(self, path: str, json: dict):
        """
        Perform POST request.

        Example:
        client.post("/items", json=payload)
        """
        return requests.post(
            f"{self.base_url}{path}",
            json=json,
            headers=self.headers,
        )
