import threading
from config.users.user_pools import ADMIN_USERS, EDITOR_USERS, VIEWER_USERS


class UserPoolManager:
    """
    Thread-safe role-based user leasing.
    """

    def __init__(self):
        self._lock = threading.Lock()
        self._leased = set()

        self._pools = {
            "ADMIN": ADMIN_USERS,
            "EDITOR": EDITOR_USERS,
            "VIEWER": VIEWER_USERS,
        }

    def acquire(self, role: str) -> dict:
        with self._lock:
            for user in self._pools[role]:
                user_key = f"{role}:{user['email']}"
                if user_key not in self._leased:
                    self._leased.add(user_key)
                    user["id"] = user["email"]  # stable identifier
                    return user

            raise RuntimeError(f"No available users for role {role}")

    def release(self, user: dict):
        with self._lock:
            user_key = f"{user['role']}:{user['email']}"
            self._leased.discard(user_key)
