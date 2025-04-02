#Unit test
#tests.py
from django.test import TestCase

# Create your tests here.
import pytest
from django.contrib.auth.models import User
from withdrawal.models import Wallet, WithdrawalRequest

@pytest.mark.django_db
def test_create_valid_withdrawal():
    #Test if a valid withdrawal request is created successfully
    user = User.objects.create_user(username="testuser", password="testpassword")
    wallet = Wallet.objects.create(associated_user=user, balance=500.00, payment_token="123abc")

    withdrawal = WithdrawalRequest.objects.create(
        associated_user=user,
        wallet=wallet,
        amount=100.00,
        wallet_address="your_offline_wallet_address_here",
        status="pending"
    )

    assert withdrawal.amount == 100.00
    assert withdrawal.status == "pending"
    assert withdrawal.wallet_address == "your_offline_wallet_address_here"
    assert withdrawal.wallet == wallet

@pytest.mark.django_db
def test_withdrawal_fails_if_insufficient_balance():
    #Test that withdrawal request fails when there is insufficient balance
    user = User.objects.create_user(username="testuser", password="testpassword")
    wallet = Wallet.objects.create(associated_user=user, balance=50.00, payment_token="123abc")

    # Try creating withdrawal larger than available balance
    withdrawal = WithdrawalRequest.objects.create(
        associated_user=user,
        wallet=wallet,
        amount=100.00,  # More than wallet balance
        wallet_address="your_offline_wallet_address_here",
        status="pending"
    )

    # Fetch updated wallet balance
    wallet.refresh_from_db()

    # Ensure balance remains the same because withdrawal should not be processed
    assert wallet.balance == 50.00, "Withdrawal should not be deducted if insufficient funds"
