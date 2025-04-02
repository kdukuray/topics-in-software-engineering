# withdrawal/tests/test_forms.py
from django.test import TestCase
from withdrawal.forms import WithdrawalForm  

class WithdrawalFormTest(TestCase):
    def test_valid_form(self):
        """Test WithdrawalForm with valid data"""
        form = WithdrawalForm(data={
            'wallet_address': 'bc1qar0srrr7xfkvy5l643lydnw9re59gtzzwfupj0',
            'amount': '50.00'
        })
        self.assertTrue(form.is_valid())

    def test_invalid_wallet_address(self):
        """Test WithdrawalForm with an invalid wallet address"""
        form = WithdrawalForm(data={'wallet_address': '', 'amount': '50.00'})
        self.assertFalse(form.is_valid())

    def test_invalid_amount(self):
        """Test WithdrawalForm with a non-numeric amount"""
        form = WithdrawalForm(data={'wallet_address': 'bc1qar0srrr7xfkvy5l643lydnw9re59gtzzwfupj0', 'amount': 'abc'})
        self.assertFalse(form.is_valid())

   