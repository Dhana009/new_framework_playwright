import os
import pytest
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

from auth.auth_cache import AuthCache
from auth.ui_login import ui_login

load_dotenv()


@pytest.fixture(scope="session")
def browser():
    """
    Phase 0 browser fixture.
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        yield browser
        browser.close()


@pytest.fixture(scope="session")
def admin_user():
    """
    Phase 0: single admin user.
    """
    return {
        "email": os.environ["ADMIN_1_EMAIL"],
        "password": os.environ["ADMIN_1_PASSWORD"],
        "role": "ADMIN",
        "id": os.environ["ADMIN_1_EMAIL"],
    }


@pytest.fixture(scope="session")
def auth_cache():
    """
    Cache UI login per user.
    """
    return AuthCache(login_func=ui_login)


@pytest.fixture
def auth_state(admin_user, auth_cache):
    """
    Ensure admin is logged in once.
    """
    if not auth_cache.exists(admin_user):
        auth_cache.login_and_store(admin_user)

    return auth_cache.get(admin_user)


@pytest.fixture
def page(browser, auth_state):
    """
    Authenticated page.
    """
    context = browser.new_context(storage_state=auth_state)
    page = context.new_page()
    yield page
    context.close()

@pytest.fixture
def auth_state(admin_user, auth_cache, browser):
    """
    Ensure admin is logged in once.
    """
    if not auth_cache.exists(admin_user):
        auth_cache.login_and_store(browser, admin_user)

    return auth_cache.get(admin_user)
