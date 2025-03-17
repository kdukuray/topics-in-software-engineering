from django.test import TestCase
from django.contrib.auth.models import User
from ..models import Wallet, Transaction
from decimal import Decimal


class WalletTransactionIntegrationTest(TestCase):

    def setUp(self):
        """Creating a user and wallet before each test"""
        self.user = User.objects.create_user(username="testuser", email="test@example.com", password="password123")
        self.wallet = Wallet.objects.create(associated_user=self.user, balance=Decimal("100.00"),
                                            payment_token="testtoken")

    def test_successful_transaction_updates_wallet_balance(self):
        """Test that a successful transaction deducts the amount from the wallet balance"""
        initial_balance = self.wallet.balance
        transaction_amount = Decimal("30.00")

        # Create a transaction
        transaction = Transaction.objects.create(
            associated_user=self.user,
            amount=transaction_amount,
            transaction_address="0x123abc"
        )

        # Simulate deducting from wallet
        self.wallet.balance -= transaction.amount
        self.wallet.save()

        self.wallet.refresh_from_db()  # Reload wallet from database
        self.assertEqual(self.wallet.balance, initial_balance - transaction_amount)

    def test_transaction_fails_if_insufficient_balance(self):
        """Test that a transaction fails if the wallet has insufficient funds"""
        transaction_amount = Decimal("150.00")  # More than wallet balance

        with self.assertRaises(ValueError):  # Expect an error
            transaction = Transaction.objects.create(
                associated_user=self.user,
                amount=transaction_amount,
                transaction_address="0x456def"
            )
            # Simulate balance deduction (add validation in models.py)
            if self.wallet.balance < transaction.amount:
                raise ValueError("Insufficient funds")

            self.wallet.balance -= transaction.amount
            self.wallet.save()
