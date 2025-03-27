# withdrawal/tests/test_e2e.py

import os
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"  # Allow synchronous DB access

from django.contrib.auth.models import User
from django.test import LiveServerTestCase
from withdrawal.models import Wallet, WithdrawalRequest
from playwright.sync_api import sync_playwright
import pytest

@pytest.mark.django_db(transaction=True)  # Ensure database transactions are isolated
class TestEndToEndWithdrawal(LiveServerTestCase):
    """
    Test the full end-to-end withdrawal process from login to successful submission.
    This test demonstrates the expected successful interaction via the user interface.
    """

    def test_end_to_end_withdrawal_request(self):
        # Step 1: Create test user and wallet
        user = User.objects.create_user(username="user", password="newpassword123")
        user.is_active = True
        user.is_staff = True  # Business owner
        user.save()

        Wallet.objects.create(associated_user=user, balance=100.00)

        # Step 2: Use Playwright to interact with the UI
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True, slow_mo=500)  # Headless for CI compatibility
            page = browser.new_page()

            # Step 3: Log in
            page.goto(f"{self.live_server_url}/login/")
            page.wait_for_load_state("networkidle")
            print(f"DEBUG: Page URL after goto: {page.url}")
            print(f"DEBUG: Page content: {page.inner_text('body')}")

            # Wait for the username field to ensure the page is loaded
            page.wait_for_selector('input[name="username"]', state="attached", timeout=10000)
            page.fill('input[name="username"]', "user")
            page.fill('input[name="password"]', "newpassword123")

            submit_button = page.locator('button:has-text("Submit")')
            print(f"DEBUG: Submit button count: {submit_button.count()}")
            if submit_button.count() == 0:
                page.screenshot(path="debug_login_no_submit.png")
                print(f"DEBUG: HTML content: {page.inner_html('body')}")
                raise AssertionError("No submit button found on login page!")

            is_disabled = submit_button.evaluate("el => el.hasAttribute('disabled')")
            print(f"DEBUG: Is submit button disabled? {is_disabled}")
            if is_disabled:
                page.screenshot(path="debug_login_disabled_submit.png")
                raise AssertionError("Submit button is disabled on login page!")

            submit_button.click()
            page.wait_for_load_state("networkidle")

            # Verify successful login redirection
            assert "Business Owner Dashboard" in page.inner_text("body"), "Login failed or incorrect redirection"

            # Step 4: Navigate to Withdrawal Page
            page.click("text=Withdraw Funds")
            page.wait_for_load_state("networkidle")

            # Verify withdrawal page loads
            assert "Withdraw Funds" in page.inner_text("body"), "Failed to load withdrawal page"

            # Step 5: Fill and Submit Withdrawal Form
            page.fill('input[name="wallet_address"]', "bc1qar0srrr7xfkvy5l643lydnw9re59gtzzwfupj0")
            page.fill('input[name="amount"]', "50.00")

            print(f"DEBUG: Before submitting withdrawal form, page URL: {page.url}")
            print(f"DEBUG: Withdrawal form content: {page.inner_text('body')}")
            page.click('button[type="submit"]')

            # Wait for redirection to dashboard
            page.wait_for_url(f"{self.live_server_url}/owner-dashboard/", timeout=10000)

            # Verify successful submission by checking dashboard state
            assert "Wallet Balance: $50.00" in page.inner_text("body"), "Wallet balance not updated after withdrawal"
            assert "pending" in page.inner_text("body"), "Withdrawal request not marked as pending"
            assert "bc1qar0srrr7xfkvy5l643lydnw9re59gtzzwfupj0" in page.inner_text("body"), "Wallet address not recorded"

            # Step 6: Verify withdrawal request is saved in the database
            withdrawal = WithdrawalRequest.objects.filter(associated_user=user, amount=50.00).first()
            assert withdrawal is not None, "Withdrawal request was not saved in database"

            browser.close()

