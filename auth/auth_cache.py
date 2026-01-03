class AuthCache:
    """
    Caches Playwright storage_state per user.
    Login happens once per user.
    """

    def __init__(self, login_func):
        self._login_func = login_func
        self._cache = {}

    def exists(self, user: dict) -> bool:
        return user["id"] in self._cache

    def login_and_store(self, browser, user: dict):
        storage_state = self._login_func(browser, user)
        self._cache[user["id"]] = storage_state

    def get(self, user: dict):
        return self._cache[user["id"]]
