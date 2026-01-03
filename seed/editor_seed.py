class EditorSeed:
    """
    Ensures editor-specific seed data exists.

    Characteristics:
    - Created only for EDITOR role
    - Created lazily (only if required)
    - Scoped per editor user (created_by)
    """

    REQUIRED_COUNT = 5  # Enough for editor-specific tests

    def __init__(self, api_client):
        self.api_client = api_client
        self._seeded_editors = set()

    def ensure(self, editor_user: dict):
        """
        Ensure seed exists for a specific editor.
        """
        editor_id = editor_user["id"]

        if editor_id in self._seeded_editors:
            return

        if self._seed_exists(editor_user):
            self._seeded_editors.add(editor_id)
            return

        self._create_seed(editor_user)
        self._seeded_editors.add(editor_id)

    def _seed_exists(self, editor_user: dict) -> bool:
        """
        Check if editor has sufficient items.
        """
        response = self.api_client.get(
            f"/items?created_by={editor_user['id']}&limit=1"
        )
        response.raise_for_status()

        data = response.json()
        return data["pagination"]["total"] >= self.REQUIRED_COUNT

    def _create_seed(self, editor_user: dict):
        """
        Create editor-owned seed items.
        """
        from utils.seed_builders import build_flow3_items

        payloads = build_flow3_items(created_by=editor_user["id"])

        for payload in payloads:
            self.api_client.post("/items", json=payload)
