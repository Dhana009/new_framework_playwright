import pytest
import os
from auth.auth_cache import AuthCache
from auth.api_login import admin_api_login
from api.api_client import APIClient
from seed.seed_manager import SeedManager


@pytest.fixture(scope="session")
def admin_user():
    return {
        "email": os.environ["ADMIN_1_EMAIL"],
        "password": os.environ["ADMIN_1_PASSWORD"],
        "role": "ADMIN",
    }


@pytest.fixture(scope="session")
def auth_cache():
    return AuthCache(login_func=lambda _: admin_api_login())


@pytest.fixture(scope="session")
def auth_state(admin_user, auth_cache):
    if not auth_cache.exists(admin_user):
        auth_cache.login_and_store(admin_user)
    return auth_cache.get(admin_user)


@pytest.fixture(scope="session")
def api_client(auth_state):
    return APIClient(token=auth_state)


@pytest.fixture(scope="session")
def seed_manager(api_client):
    return SeedManager(api_client)


@pytest.fixture(autouse=True)
def seed_guard(seed_manager):
    seed_manager.ensure_seed(role="ADMIN")


@pytest.fixture
def page(browser, auth_state):
    context = browser.new_context(storage_state=None)
    page = context.new_page()
    return page
