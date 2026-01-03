import os
from db.mongo_client import MongoSeedCleaner


class AdminSeed:
    """
    Ensures global seed data exists.

    Characteristics:
    - Created using ADMIN privileges
    - Created once per test session
    - Can be force-reset via SEED_RESET flag
    """

    REQUIRED_COUNT = 31  # Flow 3 requirement

    def __init__(self, api_client):
        self.api_client = api_client
        self._seeded = False

        # NEW (guarded flag)
        self._seed_reset = os.environ.get("SEED_RESET", "false").lower() == "true"

        # Mongo cleaner is only used when reset is enabled
        self._mongo_cleaner = MongoSeedCleaner() if self._seed_reset else None

    def ensure(self):
        """
        Ensure global seed exists.
        """

        # -------- NEW LOGIC (EXPLICIT + GUARDED) --------
        if self._seed_reset:
            self._reset_and_reseed()
            self._seeded = True
            return
        # ------------------------------------------------

        # -------- EXISTING LOGIC (UNCHANGED) --------
        if self._seeded:
            return

        if self._seed_exists():
            self._seeded = True
            return

        self._create_seed()
        self._seeded = True
        # --------------------------------------------

    def _seed_exists(self) -> bool:
        """
        Check if sufficient seed items exist.
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

    # -------- NEW METHODS (ISOLATED) --------
    def _reset_and_reseed(self):
        """
        Force reset seed data and recreate it.
        """
        self._mongo_cleaner.delete_all_seed_items()
        self._create_seed()
