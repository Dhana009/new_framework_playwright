import os


def test_admin_items_page_loads(page):
    frontend_url = os.environ["FRONTEND_BASE_URL"]
    page.goto(f"{frontend_url}/items", wait_until="domcontentloaded")
    page.wait_for_selector("[data-testid='items-table']", timeout=10000)
