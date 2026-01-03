class AuthCache:
    """
    Caches Playwright storage_state per user.

    Purpose:
    - Avoid repeated UI login
    - Login once per user
    - Reuse auth across tests and workers

    Scope:
    - Session-level (via fixture)
    """

    def __init__(self, login_func):
        """
        login_func: function that performs UI login
        and returns Playwright storage_state (dict)
        """
        self._login_func = login_func
        self._cache = {}

    def exists(self, user: dict) -> bool:
        """
        Check if auth state exists for user.
        """
        return user["id"] in self._cache

    def login_and_store(self, user: dict):
        """
        Perform UI login and store storage_state.
        """
        storage_state = self._login_func(user)
        self._cache[user["id"]] = storage_state

    def get(self, user: dict):
        """
        Retrieve cached storage_state for user.
        """
        return self._cache[user["id"]]
