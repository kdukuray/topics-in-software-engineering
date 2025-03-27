#test_views.py
import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from withdrawal.models import Wallet, Transaction, WithdrawalRequest

@pytest.mark.django_db
def test_dashboard_view(client):
    
    
    user = User.objects.create_user(username="testuser", password="testpassword")
    client.login(username="testuser", password="testpassword")

    response = client.get(reverse("dashboard"))

    assert response.status_code == 200
    assert "transactions" in response.context


@pytest.mark.django_db
def test_process_pending_withdrawals(client):
    #Ensure pending withdrawals are processed successfully

    user = User.objects.create_user(username="admin", password="adminpass", is_staff=True)
    wallet = Wallet.objects.create(associated_user=user, balance=500.00)
    withdrawal = WithdrawalRequest.objects.create(
        associated_user=user, wallet=wallet, amount=100.00, wallet_address="bc1qar0...", status="pending"
    )

    client.login(username="admin", password="adminpass")

    response = client.post(reverse("process_withdrawals"))

    withdrawal.refresh_from_db()
    assert response.status_code == 302  # Redirect expected
    assert withdrawal.status == "completed", "Withdrawal should be processed"

@pytest.mark.django_db
def test_dashboard_redirects_staff(client):
    #Ensure that staff users are redirected to the owner dashboard
    user = User.objects.create_user(username="staffuser", password="staffpass", is_staff=True)
    client.login(username="staffuser", password="staffpass")

    response = client.get(reverse("dashboard"))

    assert response.status_code == 302  # Should redirect staff users
    assert response.url == reverse("owner_dashboard")


@pytest.mark.django_db
def test_owner_dashboard_no_wallet(client):
    #Ensure owner dashboard redirects when no wallet exists
    user = User.objects.create_user(username="admin", password="adminpass", is_staff=True)
    client.login(username="admin", password="adminpass")

    response = client.get(reverse("owner_dashboard"))

    assert response.status_code == 302  # Should redirect if no wallet is found
    assert response.url == reverse("dashboard")  # Redirect to dashboard


@pytest.mark.django_db
def test_withdrawal_fails_if_insufficient_balance(client):
    #Ensure withdrawal request fails when the wallet has insufficient funds
    user = User.objects.create_user(username="testuser", password="testpassword")
    wallet = Wallet.objects.create(associated_user=user, balance=10.00)  # Low balance
    client.login(username="testuser", password="testpassword")

    # Follow the redirect to get the final response
    response = client.post(reverse("withdrawal_request"), {
        "wallet_address": "bc1qar0...",
        "amount": "50.00"  # More than available balance
    }, follow=True)

    # Check that the response status code is 200 (after redirect)
    assert response.status_code == 200  # After following redirect, should render a page

    # Check for the "Insufficient balance" message in the messages framework
    messages = [msg.message for msg in response.context["messages"]]
    # Use any() to check if "Insufficient balance" is a substring of any message
    assert any("Insufficient balance" in msg for msg in messages), "Expected 'Insufficient balance' message"