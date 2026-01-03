class AuthCache:
    def __init__(self, login_func):
        self._login_func = login_func
        self._cache = {}

    def exists(self, user: dict) -> bool:
        return user["email"] in self._cache

    def get(self, user: dict) -> str:
        return self._cache[user["email"]]

    def login_and_store(self, user: dict) -> str:
        token = self._login_func(user)
        self._cache[user["email"]] = token
        return token
