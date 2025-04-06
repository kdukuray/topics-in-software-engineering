from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from ..models import Wallet, Transaction
from decimal import Decimal

class ViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", email="test@example.com", password="password123")
        self.wallet = Wallet.objects.create(
            associated_user=self.user, balance=Decimal("100.00"), payment_token="abc123", company_name="TestCompany"
        )

    def test_dashboard_view(self):
        self.client.login(username="testuser", password="password123")
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Dashboard - TestCompany")
        self.assertContains(response, "Your Balance on LedgerPay: 100.00")

    def test_payment_method_view_get(self):
        self.client.login(username="testuser", password="password123")
        response = self.client.get(reverse("payment_method"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Select Preferred Payment Methods")

    def test_payment_method_view_post_success(self):
        self.client.login(username="testuser", password="password123")
        response = self.client.post(
            reverse("payment_method"),
            {"payment_methods": ["credit_card", "paypal"]}
        )
        self.assertRedirects(response, reverse("dashboard"))
        self.wallet.refresh_from_db()
        self.assertEqual(self.wallet.preferred_payment_methods, ["credit_card", "paypal"])

    def test_payment_method_view_post_no_selection(self):
        self.client.login(username="testuser", password="password123")
        response = self.client.post(reverse("payment_method"), {})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Please select at least one payment method.")

    def test_signup_view_get(self):
        response = self.client.get(reverse("signup"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "form")

    def test_signup_view_post_success(self):
        response = self.client.post(
            reverse("signup"),
            {
                "username": "newuser",
                "email": "newuser@example.com",
                "password1": "VeryComplexPassword123!@#",
                "password2": "VeryComplexPassword123!@#",
                "balance": "50.00",
                "payment_token": "xyz789",
                "company_name": "NewUserCompany"
            }
        )
        if response.status_code != 302:
            form = response.context['form']
            print(form.errors)
        self.assertRedirects(response, reverse("login"))
        self.assertTrue(User.objects.filter(username="newuser").exists())