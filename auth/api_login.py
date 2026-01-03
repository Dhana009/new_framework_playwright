import requests
import os


def api_login(user: dict) -> str:
    response = requests.post(
        f"{os.environ['BACKEND_BASE_URL']}/auth/login",
        json={
            "email": user["email"],
            "password": user["password"]
        },
        timeout=10
    )

    response.raise_for_status()
    return response.json()["access_token"]
