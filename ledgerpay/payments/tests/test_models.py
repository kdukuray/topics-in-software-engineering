from django.test import TestCase
from django.contrib.auth.models import User
from ..models import  Wallet, Transaction
from decimal import Decimal

class WalletModelTest(TestCase):

    def setUp(self):
        """Creating a test user before each test"""
        self.user = User.objects.create_user(username="testuser", email="test@example.com", password="password123")

    def test_create_wallet_successfully(self):
        """Test creating a wallet with valid data"""
        wallet = Wallet.objects.create(associated_user=self.user, balance=Decimal("100.50"), payment_token="abc123xyz")
        self.assertEqual(wallet.associated_user, self.user)
        self.assertEqual(wallet.balance, Decimal("100.50"))
        self.assertEqual(wallet.payment_token, "abc123xyz")

    def test_wallet_str_method(self):
        """Test the string representation of the Wallet model"""
        wallet = Wallet.objects.create(associated_user=self.user, balance=Decimal("50.00"), payment_token="xyz987abc")
        self.assertEqual(str(wallet), "test@example.com's Wallet")

    def test_create_wallet_with_negative_balance(self):
        """Test creating a wallet with a negative balance should raise an error"""
        with self.assertRaises(ValueError):
            Wallet.objects.create(associated_user=self.user, balance=Decimal("-10.00"), payment_token="invalid")


class TransactionModelTest(TestCase):

    def setUp(self):
        """Createing a test user before each test"""
        self.user = User.objects.create_user(username="testuser", email="test@example.com", password="password123")

    def test_create_transaction_successfully(self):
        """Test creating a transaction with valid data"""
        transaction = Transaction.objects.create(
            associated_user=self.user, amount=Decimal("25.75"), transaction_address="0x123abc"
        )
        self.assertEqual(transaction.associated_user, self.user)
        self.assertEqual(transaction.amount, Decimal("25.75"))
        self.assertEqual(transaction.transaction_address, "0x123abc")

    def test_transaction_str_method(self):
        """Test the string representation of the Transaction model"""
        transaction = Transaction.objects.create(
            associated_user=self.user, amount=Decimal("99.99"), transaction_address="0x456def"
        )
        self.assertEqual(str(transaction), "transaction of $99.99 to test@example.com")

    def test_create_transaction_with_negative_amount(self):
        """Test creating a transaction with a negative amount should raise an error"""
        with self.assertRaises(ValueError):
            Transaction.objects.create(associated_user=self.user, amount=Decimal("-5.00"), transaction_address="invalid")

