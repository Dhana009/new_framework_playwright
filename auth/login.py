from playwright.sync_api import Page


def api_login(user: dict) -> dict:
    """
    Perform UI login using Playwright and return storage_state.

    Input:
    - user: dict with credentials (email, password)

    Output:
    - Playwright storage_state (dict)

    Notes:
    - Used only for UI authentication
    - No API tokens involved
    - Called once per user and cached
    """

    # NOTE:
    # The Page object is created internally by Playwright
    # via a temporary browser context for login only.

    from playwright.sync_api import sync_playwright
    import os

    FRONTEND_BASE_URL = os.environ["FRONTEND_BASE_URL"]

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        # Navigate to login page
        page.goto(FRONTEND_BASE_URL)

        # --- LOGIN FLOW (adjust selectors to your app) ---
        page.fill("input[name='email']", user["email"])
        page.fill("input[name='password']", user["password"])
        page.click("button[type='submit']")

        # Wait until login completes (dashboard or any post-login element)
        page.wait_for_load_state("networkidle")

        # Capture storage state
        storage_state = context.storage_state()

        browser.close()

    return storage_state
