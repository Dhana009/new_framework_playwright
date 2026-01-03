class AdminSeed:
    """
    Ensures global seed data exists.

    Characteristics:
    - Created using ADMIN privileges
    - Created once per test session
    - Shared across all roles
    """

    REQUIRED_COUNT = 31  # Flow 3 requirement (pagination)

    def __init__(self, api_client):
        self.api_client = api_client
        self._seeded = False

    def ensure(self):
        """
        Ensure global seed exists.
        """
        if self._seeded:
            return

        if self._seed_exists():
            self._seeded = True
            return

        self._create_seed()
        self._seeded = True

    def _seed_exists(self) -> bool:
        """
        Check if sufficient items exist.
        Uses pagination.total from backend response.
        """
        response = self.api_client.get("/items?limit=1")
        response.raise_for_status()

        data = response.json()
        return data["pagination"]["total"] >= self.REQUIRED_COUNT

    def _create_seed(self):
        """
        Create global seed items.
        """
        from utils.seed_builders import build_flow3_items

        payloads = build_flow3_items()

        for payload in payloads:
            self.api_client.post("/items", json=payload)
