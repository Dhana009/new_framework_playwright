"""
Pytest configuration file - contains shared fixtures for all tests.
Acts as the control plane for:
- role resolution
- user leasing
- auth reuse (UI)
- seed enforcement (API)
- browser context creation
"""

import os
import pytest
from dotenv import load_dotenv

from config.users.user_pool_manager import UserPoolManager
from auth.auth_cache import AuthCache
from auth.login import api_login              # UI / Playwright login
from auth.api_login import admin_api_login    # API login for seed
from api.api_client import APIClient
from seed.seed_manager import SeedManager

# ------------------------------------------------------------------
# Environment loading (LOCAL: .env | CI: injected env vars)
# ------------------------------------------------------------------

load_dotenv()

# ------------------------------------------------------------------
# Role resolution
# ------------------------------------------------------------------

@pytest.fixture
def test_role(request):
    """
    Resolve role required by the test via markers.
    Default role: ADMIN
    """
    if request.node.get_closest_marker("admin"):
        return "ADMIN"

    if request.node.get_closest_marker("editor"):
        return "EDITOR"

    if request.node.get_closest_marker("viewer"):
        return "VIEWER"

    return "ADMIN"


# ------------------------------------------------------------------
# Session-level infrastructure
# ------------------------------------------------------------------

@pytest.fixture(scope="session")
def user_pool():
    """
    Manages role-based user leasing (ADMIN / EDITOR / VIEWER).
    """
    return UserPoolManager()


@pytest.fixture(scope="session")
def auth_cache():
    """
    Caches Playwright authentication state per user.
    UI login happens once per user.
    """
    return AuthCache(login_func=api_login)


@pytest.fixture(scope="session")
def api_client():
    """
    Stateless API client for seed operations.
    Authenticated using ADMIN JWT token.
    """
    backend_url = os.environ["BACKEND_BASE_URL"]
    admin_email = os.environ["ADMIN_EMAIL"]
    admin_password = os.environ["ADMIN_PASSWORD"]

    access_token = admin_api_login(
        backend_base_url=backend_url,
        email=admin_email,
        password=admin_password,
    )

    return APIClient(
        backend_base_url=backend_url,
        access_token=access_token,
    )


@pytest.fixture(scope="session")
def seed_manager(api_client):
    """
    Orchestrates role-aware seed enforcement.
    """
    return SeedManager(api_client)


# ------------------------------------------------------------------
# Per-test orchestration
# ------------------------------------------------------------------

@pytest.fixture
def leased_user(test_role, user_pool):
    """
    Lease a user based on role for the duration of the test.
    """
    user = user_pool.acquire(test_role)
    yield user
    user_pool.release(user)


@pytest.fixture
def auth_state(leased_user, auth_cache):
    """
    Ensure Playwright authentication exists for the leased user.
    Login only happens if auth is missing.
    """
    if not auth_cache.exists(leased_user):
        auth_cache.login_and_store(leased_user)

    return auth_cache.get(leased_user)


@pytest.fixture(autouse=True)
def seed_guard(test_role, leased_user, seed_manager):
    """
    Ensure required seed data exists before each test.
    """
    seed_manager.ensure_seed(
        role=test_role,
        user=leased_user,
    )


# ------------------------------------------------------------------
# Browser context & page
# ------------------------------------------------------------------

@pytest.fixture
def page(browser, auth_state):
    """
    Create an authenticated browser context and page.
    """
    context = browser.new_context(storage_state=auth_state)
    page = context.new_page()
    yield page
    context.close()
