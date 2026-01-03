import os
import requests


def admin_api_login() -> str:
    """
    Login as admin via backend API and return JWT token.
    """
    backend_url = os.environ["BACKEND_BASE_URL"]
    email = os.environ["ADMIN_1_EMAIL"]
    password = os.environ["ADMIN_1_PASSWORD"]

    response = requests.post(
        f"{backend_url}/auth/login",
        json={"email": email, "password": password},
        timeout=10,
    )
    response.raise_for_status()

    data = response.json()
    return data["token"]
