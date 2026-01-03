import os
import requests


def admin_api_login() -> str:
    response = requests.post(
        f"{os.environ['BACKEND_BASE_URL']}/auth/login",
        json={
            "email": os.environ["ADMIN_1_EMAIL"],
            "password": os.environ["ADMIN_1_PASSWORD"],
        },
        timeout=10,
    )
    response.raise_for_status()
    return response.json()["token"]
