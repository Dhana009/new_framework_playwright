import threading

from config.users.user_pools import (
    ADMIN_USERS,
    EDITOR_USERS,
    VIEWER_USERS,
)


class UserPoolManager:
    """
    Manages role-based user leasing.

    Guarantees:
    - A user is leased to only one test at a time
    - Role constraints are respected
    - Users are returned after test completion
    """

    def __init__(self):
        self._lock = threading.Lock()

        self._pools = {
            "ADMIN": list(ADMIN_USERS),
            "EDITOR": list(EDITOR_USERS),
            "VIEWER": list(VIEWER_USERS),
        }

        self._leased = {
            "ADMIN": set(),
            "EDITOR": set(),
            "VIEWER": set(),
        }

    def acquire(self, role: str) -> dict:
        """
        Acquire a user for the given role.

        Raises:
            RuntimeError if no user is available.
        """
        with self._lock:
            for user in self._pools.get(role, []):
                if user["id"] not in self._leased[role]:
                    self._leased[role].add(user["id"])
                    return user

            raise RuntimeError(f"No available users for role: {role}")

    def release(self, user: dict):
        """
        Release a previously leased user.
        """
        role = user["role"]

        with self._lock:
            self._leased[role].discard(user["id"])
