import os
from db.mongo_client import MongoSeedCleaner
from auth.api_login import api_login
from api.api_client import APIClient


class EditorSeed:
    """
    Ensures editor-specific seed data exists.

    Characteristics:
    - Created only for EDITOR role
    - Created lazily (only if missing)
    - Scoped per editor (created_by)
    - Can be force-reset via SEED_RESET flag
    """

    REQUIRED_COUNT = 5  # Enough for editor-specific tests

    def __init__(self):
        self._seeded_editors = set()

        # NEW (guarded flag)
        self._seed_reset = os.environ.get("SEED_RESET", "false").lower() == "true"

        # Mongo cleaner used only when reset is enabled
        self._mongo_cleaner = MongoSeedCleaner() if self._seed_reset else None

    def ensure(self, editor_user: dict):
        """
        Ensure seed exists for a specific editor.
        """
        editor_id = editor_user["id"]

        # -------- NEW LOGIC (EXPLICIT + GUARDED) --------
        if self._seed_reset:
            self._reset_and_reseed(editor_user)
            self._seeded_editors.add(editor_id)
            return
        # ------------------------------------------------

        # -------- EXISTING LOGIC (UNCHANGED) --------
        if editor_id in self._seeded_editors:
            return

        if self._seed_exists(editor_user):
            self._seeded_editors.add(editor_id)
            return

        self._create_seed(editor_user)
        self._seeded_editors.add(editor_id)
        # --------------------------------------------

    def _seed_exists(self, editor_user: dict) -> bool:
        """
        Check if editor has sufficient seed items.
        """
        api_client = self._get_editor_api_client(editor_user)

        response = api_client.get(
            f"/items?created_by={editor_user['id']}&limit=1"
        )
        response.raise_for_status()

        data = response.json()
        return data["pagination"]["total"] >= self.REQUIRED_COUNT

    def _create_seed(self, editor_user: dict):
        """
        Create editor-owned seed items using EDITOR API login.
        """
        api_client = self._get_editor_api_client(editor_user)

        from utils.seed_builders import build_flow3_items
        payloads = build_flow3_items(created_by=editor_user["id"])

        for payload in payloads:
            api_client.post("/items", json=payload)

    # -------- NEW METHODS (ISOLATED) --------
    def _reset_and_reseed(self, editor_user: dict):
        """
        Force reset editor seed data and recreate it.
        """
        self._mongo_cleaner.delete_editor_seed_items(editor_user["id"])
        self._create_seed(editor_user)

    def _get_editor_api_client(self, editor_user: dict) -> APIClient:
        """
        Lazily create an API client authenticated as the editor.
        """
        token = api_login(editor_user)
        return APIClient(token)
