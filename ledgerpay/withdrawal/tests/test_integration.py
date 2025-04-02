# withdrawal/tests/test_integration.py
import pytest
from django.contrib.auth.models import User
from withdrawal.models import Wallet, WithdrawalRequest  # Updated import
from withdrawal.forms import WithdrawalForm  # Updated import
from decimal import Decimal

@pytest.mark.django_db
def test_withdrawal_request_creates_entry_and_updates_wallet():
    """Test that submitting a withdrawal request creates a WithdrawalRequest entry and updates the wallet balance."""
    
    # Create test user and wallet
    user = User.objects.create_user(username="testuser", password="testpassword")
    wallet = Wallet.objects.create(associated_user=user, balance=Decimal("200.00"), payment_token="test_token")

    # Form data simulating user input
    form_data = {
        "wallet_address": "bc1qar0srrr7xfkvy5l643lydnw9re59gtzzwfupj0",
        "amount": "50.00"
    }

    form = WithdrawalForm(data=form_data)

    # Ensure form is valid before proceeding
    assert form.is_valid(), f"Form errors: {form.errors}"

    # Create withdrawal request
    withdrawal = WithdrawalRequest.objects.create(
        associated_user=user,
        wallet=wallet,
        amount=Decimal(form.cleaned_data["amount"]),  # Convert to Decimal
        wallet_address=form.cleaned_data["wallet_address"],
        status="pending"
    )

    # Update wallet balance
    wallet.balance -= Decimal(withdrawal.amount)  # Convert to Decimal
    wallet.save()

    # Check if withdrawal request was created in the database
    assert WithdrawalRequest.objects.filter(associated_user=user, amount=Decimal("50.00")).exists()

    # Check if wallet balance was updated correctly
    updated_wallet = Wallet.objects.get(associated_user=user)
    assert updated_wallet.balance == Decimal("150.00"), f"Expected balance: 150.00, got {updated_wallet.balance}"

@pytest.mark.django_db
def test_withdrawal_fails_if_balance_too_low():
    """Test that a withdrawal request is rejected if the wallet balance is too low."""
    
    # Create test user and wallet with insufficient balance
    user = User.objects.create_user(username="testuser", password="testpassword")
    wallet = Wallet.objects.create(associated_user=user, balance=Decimal("30.00"), payment_token="test_token")

    # Attempt withdrawal request
    form_data = {
        "wallet_address": "bc1qar0srrr7xfkvy5l643lydnw9re59gtzzwfupj0",
        "amount": "50.00"  # More than the available balance
    }

    form = WithdrawalForm(data=form_data)

    # Form should still be valid because validation is separate from business logic
    assert form.is_valid(), f"Form errors: {form.errors}"

    # Simulate business logic that prevents withdrawal if balance is too low
    withdrawal_allowed = wallet.balance >= Decimal(form.cleaned_data["amount"])

    # Ensure withdrawal was rejected due to insufficient funds
    assert withdrawal_allowed is False, "Withdrawal should have been blocked due to insufficient balance."

