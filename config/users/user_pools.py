import os


def _load_users(role: str) -> list[dict]:
    """
    Load users for a role from ENV.
    Pattern: ROLE_1_EMAIL / ROLE_1_PASSWORD
    """
    users = []
    index = 1

    while True:
        email = os.environ.get(f"{role}_{index}_EMAIL")
        password = os.environ.get(f"{role}_{index}_PASSWORD")

        if not email or not password:
            break

        users.append({
            "email": email,
            "password": password,
            "role": role
        })

        index += 1

    if not users:
        raise RuntimeError(f"No users found for role {role}")

    return users


ADMIN_USERS = _load_users("ADMIN")
EDITOR_USERS = _load_users("EDITOR")
VIEWER_USERS = _load_users("VIEWER")
