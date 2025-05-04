from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Wallet, Transaction
from django.views.decorators.http import require_POST
from decimal import Decimal
from django.http import JsonResponse
from .utils import can_transfer
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

# Create your views here.
@login_required(login_url="login")
def dashboard(request):
    all_user_transactions = Transaction.objects.filter(associated_user=request.user)
    return render(request, 'payments/dashboard.html', context={"transactions": all_user_transactions})




@require_POST
@login_required
def transfer_funds(request):
    sender = request.user
    recipient_email = request.POST.get("recipient_email")
    amount_str = request.POST.get("amount")
    tx_address = request.POST.get("transaction_address")

    # Validate and parse amount
    try:
        amount = Decimal(amount_str)
    except:
        return JsonResponse({"error": "Invalid amount format"}, status=400)

    # Get wallets and users
    sender_wallet = get_object_or_404(Wallet, associated_user=sender)
    recipient_user = get_object_or_404(User, email=recipient_email)
    recipient_wallet = get_object_or_404(Wallet, associated_user=recipient_user)

    # Check transfer validity
    if not can_transfer(sender_wallet.balance, amount):
        return JsonResponse({"error": "Insufficient or invalid transfer amount"}, status=400)

    # Perform transaction
    sender_wallet.balance -= amount
    recipient_wallet.balance += amount
    sender_wallet.save()
    recipient_wallet.save()

    Transaction.objects.create(
        amount=amount,
        transaction_address=tx_address or "Internal Transfer",
        associated_user=recipient_user
    )

    return JsonResponse({
        "message": f"Transferred ${amount} to {recipient_email} successfully.",
        "new_balance": str(sender_wallet.balance)
    })