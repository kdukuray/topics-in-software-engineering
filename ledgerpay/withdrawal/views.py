from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Wallet, Transaction
from .forms import WithdrawalForm
from django.contrib import messages
from .models import WithdrawalRequest


# Create your views here.

@login_required(login_url="login")
def dashboard(request):
    if request.user.is_staff:  # Check if user is a business owner
        return redirect("owner_dashboard")  # Redirect to owner dashboard
    all_user_transactions = Transaction.objects.filter(associated_user=request.user)
    return render(request, 'withdrawal/dashboard.html', context={"transactions": all_user_transactions})
#Alex

@login_required(login_url="login")
def owner_dashboard(request):
    try:
        user_wallet = Wallet.objects.get(associated_user=request.user)
    except Wallet.DoesNotExist:
        messages.error(request, "No wallet found. Please set up a wallet first.")
        return redirect("dashboard")

    all_withdrawals = WithdrawalRequest.objects.filter(wallet=user_wallet)

    if request.method == "POST":
        all_withdrawals.filter(status="pending").update(status="completed")
        messages.success(request, "All pending withdrawals have been processed.")
        return redirect("owner_dashboard")

    return render(request, "withdrawal/owner_dashboard.html", {"wallet": user_wallet, "withdrawals": all_withdrawals})



#withdrawal request view
@login_required(login_url="login")
def withdrawal_request(request):
    user_wallet = Wallet.objects.get(associated_user=request.user)

    if request.method == 'POST':
        form = WithdrawalForm(request.POST)
        if form.is_valid():
            wallet_address = form.cleaned_data['wallet_address']
            amount = form.cleaned_data['amount']

            # Ensure sufficient balance before processing withdrawal
            if user_wallet.balance < amount:
                messages.error(request, "Insufficient balance.")
                return redirect("withdrawal_request")

            # Create a withdrawal request (not a transaction)
            withdrawal = WithdrawalRequest.objects.create(
                associated_user=request.user,
                wallet=user_wallet,
                amount=amount,
                wallet_address=wallet_address,
                status="pending"
            )

            # Deduct the amount from the user's wallet balance
            user_wallet.balance -= amount
            user_wallet.save()

            messages.success(request, 'Your withdrawal request is being processed.')

            # Redirect based on user type
            if request.user.is_staff:  # Assuming business owners have `is_staff=True`
                return redirect('owner_dashboard')  # Redirect business owners
            else:
                return redirect('dashboard')  # Redirect regular users

    else:
        form = WithdrawalForm()

    return render(request, 'withdrawal/withdrawal_form.html', {'form': form})




# Function to simulate withdrawal processing
def process_withdrawal(withdrawal):
    """
    Simulates sending crypto to an offline wallet.
    In production, this should call an actual API.
    """
    print(f"Processing withdrawal of ${withdrawal.amount} to {withdrawal.wallet_address}")
    withdrawal.status = "completed"  # Simulate a successful transfer
    withdrawal.save()


# Admin view to process pending withdrawals
@login_required(login_url="login")
def process_pending_withdrawals(request):
    pending_withdrawals = WithdrawalRequest.objects.filter(status="pending")

    for withdrawal in pending_withdrawals:
        process_withdrawal(withdrawal)

    messages.success(request, "All pending withdrawals have been processed.")
    return redirect("dashboard")