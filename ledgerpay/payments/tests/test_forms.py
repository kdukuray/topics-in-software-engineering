from django.test import TestCase
from payments.forms import add_user_and_wallet
from decimal import Decimal

class FormsTest(TestCase):
    def test_add_user_and_wallet_valid(self):
        form_data = {
            "username": "testuser4",
            "email": "testEmail4@gmail.com",
            "password1": "password4Test",
            "password2": "password4Test",
            "company_name": "company name 4 test",
            "payment_token": "tokenest4"
        }
        form = add_user_and_wallet(data=form_data)
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertEqual(user.username, "testuser4")
        self.assertEqual(user.email, "testEmail4@gmail.com")
        self.assertTrue(user.check_password("password4Test"))
        self.assertEqual(user.wallet.company_name, "company name 4 test")
        self.assertEqual(user.wallet.payment_token, "tokenest4")
        self.assertEqual(user.wallet.balance, Decimal("0.00"))

    def test_add_user_and_wallet_invalid_password(self):
        form_data = {
            "username": "testuser4",
            "email": "testEmail4@gmail.com",
            "password1": "password4Test",
            "password2": "differentpassword",  # Mismatched password
            "company_name": "company name 4 test",
            "payment_token": "tokenest4"
        }
        form = add_user_and_wallet(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("password2", form.errors)

    def test_add_user_and_wallet_missing_company_name(self):
        form_data = {
            "username": "testuser4",
            "email": "testEmail4@gmail.com",
            "password1": "password4Test",
            "password2": "password4Test",
            "payment_token": "tokenest4"
        }
        form = add_user_and_wallet(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("company_name", form.errors)

    def test_add_user_and_wallet_missing_payment_token(self):
        form_data = {
            "username": "testuser4",
            "email": "testEmail4@gmail.com",
            "password1": "password4Test",
            "password2": "password4Test",
            "company_name": "company name 4 test",
            
        }
        form = add_user_and_wallet(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("payment_token", form.errors)