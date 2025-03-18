"""These are our end-to-end tests for signing in """

from playwright.sync_api import sync_playwright

def test_login_django_admin():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Navigate to the Django admin login page
        page.goto("http://127.0.0.1:8000/admin/")

        # Fill in login credentials
        page.fill("input[name='username']", "user")
        page.fill("input[name='password']", "password")

        # Submit login form
        page.press("input[name='password']", "Enter")

        # Wait for the admin page to load
        page.wait_for_selector("body")

        # Assert that login was successful by checking for a known element
        assert "Site administration" in page.inner_text("body"), "❌ Login failed!"

        browser.close()
