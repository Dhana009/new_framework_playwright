import os


def ui_login(browser, user: dict) -> dict:
    """
    Perform UI login using an existing browser and return storage_state.
    """
    frontend_url = os.environ["FRONTEND_BASE_URL"]

    context = browser.new_context()
    page = context.new_page()

    page.goto(f"{frontend_url}/login", wait_until="domcontentloaded")

    page.fill("input[type='email']", user["email"])
    page.fill("input[type='password']", user["password"])
    page.click("button[type='submit']")

    page.wait_for_function(
        "window.location.pathname !== '/login'",
        timeout=10000
    )

    storage_state = context.storage_state()
    context.close()

    return storage_state
