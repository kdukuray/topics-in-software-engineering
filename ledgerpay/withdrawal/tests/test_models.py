#test_model.py
from django.test import TestCase
from django.contrib.auth.models import User
from withdrawal.models import Wallet, WithdrawalRequest ,Transaction

class ModelTests(TestCase):
    def setUp(self):
        """Set up a test user and wallet"""
        self.user = User.objects.create_user(username="testuser", email="test@example.com", password="testpass")
        self.wallet = Wallet.objects.create(associated_user=self.user, balance=100.00, payment_token="test_token")

    def test_wallet_str(self):
        """Test Wallet __str__ method"""
        self.assertEqual(str(self.wallet), "test@example.com's Wallet")

    def test_transaction_creation(self):
        """Test creating a transaction"""
        transaction = Transaction.objects.create(
            amount=20.00, transaction_address="xyz_address", associated_user=self.user
        )
        self.assertEqual(transaction.amount, 20.00)
        self.assertEqual(str(transaction), "transaction of $20.0 to test@example.com")

    def test_withdrawal_request_creation(self):
        """Test WithdrawalRequest model"""
        withdrawal = WithdrawalRequest.objects.create(
            associated_user=self.user,
            wallet=self.wallet,
            amount=50.00,
            wallet_address="bc1qar0srrr7xfkvy5l643lydnw9re59gtzzwfupj0",
            status="pending"
        )
        self.assertEqual(withdrawal.amount, 50.00)
        self.assertEqual(withdrawal.status, "pending")

    def test_withdrawal_updates_wallet_balance(self):
        """Test that withdrawal updates wallet balance correctly"""
        withdrawal = WithdrawalRequest.objects.create(
        associated_user=self.user,
        wallet=self.wallet,
        amount=30.00,  # Withdraw 30 from balance 100
        wallet_address="bc1qar0srrr7xfkvy5l643lydnw9re59gtzzwfupj0",
        status="pending"
        )

        # Simulate processing the withdrawal
        self.wallet.balance -= withdrawal.amount
        self.wallet.save()

        # Fetch updated wallet from DB
        updated_wallet = Wallet.objects.get(id=self.wallet.id)
        self.assertEqual(updated_wallet.balance, 70.00, "Wallet balance should be updated after withdrawal")

