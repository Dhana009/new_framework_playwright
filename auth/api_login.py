import requests


def admin_api_login(backend_base_url: str, email: str, password: str) -> str:
    """
    Logs in to backend using ADMIN credentials and returns JWT access token.

    Uses:
    POST {BACKEND_BASE_URL}/auth/login

    Returns:
    - access_token (string)

    Notes:
    - Stateless
    - No refresh-token handling (intentional)
    - Used only for API-based seed operations
    """

    url = f"{backend_base_url}/auth/login"

    payload = {
        "email": email,
        "password": password
    }

    response = requests.post(url, json=payload)

    # Fail fast if login fails
    response.raise_for_status()

    data = response.json()

    if "access_token" not in data:
        raise RuntimeError("API login failed: access_token not found in response")

    return data["access_token"]
