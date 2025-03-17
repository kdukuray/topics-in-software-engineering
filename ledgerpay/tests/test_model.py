# wallet_app/tests.py

from django.test import TestCase
from django.contrib.auth.models import User
from payments.models import Transaction
from payments.models import Wallet



class WalletModelTest(TestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(
            username='adama1945',
            email='adama1945@example.com',
            password='test123'
        )
        # Create a wallet for that user
        self.wallet = Wallet.objects.create(
            associated_user=self.user,
            balance=100.00,
            payment_token='ABC123'
        )

    def test_wallet_creation(self):
        """Test that the Wallet was created correctly."""
        self.assertEqual(self.wallet.associated_user.username, 'adama1945')
        self.assertEqual(self.wallet.balance, 100.00)
        self.assertEqual(self.wallet.payment_token, 'ABC123')

    def test_wallet_str(self):
        """Test the string representation of the Wallet model."""
        self.assertEqual(
            str(self.wallet),
            "adama1945@example.com's Wallet"
        )

class TransactionModelTest(TestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(
            username='adama1945',
            email='adama1945@example.com',
            password='test123'
        )
        #atransaction for that user
        self.transaction = Transaction.objects.create(
            associated_user=self.user,
            amount=50.00,
            transaction_address='ADDRESS123'
        )

    def test_transaction_creation(self):
        """Test that the Transaction was created correctly."""
        self.assertEqual(self.transaction.associated_user.username, 'adama1945')
        self.assertEqual(self.transaction.amount, 50.00)
        self.assertEqual(self.transaction.transaction_address, 'ADDRESS123')

    def test_auto_now_add(self):
        """Test that transaction_date is automatically set on creation."""
        self.assertIsNotNone(self.transaction.transaction_date)

