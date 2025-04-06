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

def test_select_payment():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Log in to the admin panel first
        page.goto("http://127.0.0.1:8000/admin/")
        page.fill("input[name='username']", "user")
        page.fill("input[name='password']", "password")
        page.press("input[name='password']", "Enter")
        page.wait_for_selector("body")
        assert "Site administration" in page.inner_text("body"), "❌ Login failed!"

        # Navigate to the dashboard
        page.goto("http://127.0.0.1:8000/")

        # Click the "Select Payment Methods" button
        page.click("text=Select Payment Methods")

        # Wait for the payment method page to load
        page.wait_for_selector("h2:text('Select Preferred Payment Methods')")

        # Select a payment method (e.g., Credit Card)
        page.check("input[value='credit_card']")

        page.click("button:text('Proceed')")

        page.wait_for_selector("h1")  

        h1_text = page.inner_text("h1")
        assert "LedgerPay" in h1_text, f"❌ Expected 'Dashboard' in h1, got '{h1_text}'!"

        browser.close()
def test_signup():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Generate a unique username using a timestamp
        import time
        unique_username = f"newuser_e2e_{int(time.time())}"
        unique_email = f"newuser_e2e_{int(time.time())}@example.com"

        page.goto("http://127.0.0.1:8000/signup/")

        page.fill("input[name='username']", unique_username)
        page.fill("input[name='email']", unique_email)
        page.fill("input[name='password1']", "Password123!@#")
        page.fill("input[name='password2']", "Password123!@#")
        page.fill("input[name='company_name']", "E2E Test Company")
        page.fill("input[name='payment_token']", "e2e_token_123")

        page.click("button[type='submit']")

        try:
            page.wait_for_url("http://127.0.0.1:8000/login/", timeout=10000)
        except Exception as e:
            error = page.query_selector("ul.errorlist")
            if error:
                print(f"Form errors: {error.inner_text()}")
            else:
                print("No form errors found. Page content:")
                print(page.content())
            raise e

        assert page.url == "http://127.0.0.1:8000/login/", "❌ Failed to redirect to login page after signup!"

        browser.close()