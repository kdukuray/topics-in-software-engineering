from playwright.sync_api import sync_playwright

def test_registration():
    with sync_playwright() as p:
        # Launch browser and navigate to the registration page
        browser = p.chromium.launch(headless=False)  # Set headless=True for no UI
        page = browser.new_page()
        page.goto("http://localhost:8000/register")  # URL of your registration page

        # Fill in the form fields
        page.fill('input[name="name"]', 'John Doe')
        page.fill('input[name="email"]', 'john@example.com')
        page.fill('input[name="password"]', 'Password123')

        # Submit the form
        page.click('button[type="submit"]')

        # Wait for the response and verify success
        page.wait_for_selector('text=Registration successful!')

        # Close browser
        browser.close()

