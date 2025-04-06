from django.test import TestCase
from django.urls import reverse, resolve
from payments.views import dashboard, signup, payment_method
from django.contrib.auth.views import LoginView, LogoutView

class UrlsTest(TestCase):
    def test_dashboard_url(self):
        url = reverse("dashboard")
        self.assertEqual(url, "/")
        self.assertEqual(resolve(url).func, dashboard)

    def test_login_url(self):
        url = reverse("login")
        self.assertEqual(url, "/login/")
        self.assertEqual(resolve(url).func.view_class, LoginView)

    def test_logout_url(self):
        url = reverse("logout")
        self.assertEqual(url, "/logout")
        self.assertEqual(resolve(url).func.view_class, LogoutView)

    def test_signup_url(self):
        url = reverse("signup")
        self.assertEqual(url, "/signup/")
        self.assertEqual(resolve(url).func, signup)

    def test_payment_method_url(self):
        url = reverse("payment_method")
        self.assertEqual(url, "/payment/")
        self.assertEqual(resolve(url).func, payment_method)