from seed.admin_seed import AdminSeed
from seed.editor_seed import EditorSeed


class SeedManager:
    """
    Orchestrates role-aware seed enforcement.

    Responsibilities:
    - Ensure global admin seed exists once
    - Ensure editor-specific seed exists lazily
    - Skip seed creation for viewer
    """

    def __init__(self, api_client):
        self._admin_seed = AdminSeed(api_client)
        self._editor_seed = EditorSeed(api_client)

    def ensure_seed(self, role: str, user: dict):
        """
        Ensure required seed data exists before test execution.
        """
        if role == "ADMIN":
            self._admin_seed.ensure()

        elif role == "EDITOR":
            self._admin_seed.ensure()
            self._editor_seed.ensure(user)

        elif role == "VIEWER":
            # Viewer cannot create data
            # Assumes admin seed already exists
            self._admin_seed.ensure()

        else:
            raise ValueError(f"Unknown role: {role}")
