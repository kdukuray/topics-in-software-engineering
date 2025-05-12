from idlelib.pyparse import trans

from django.db.models.expressions import result
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from .utils import check_transaction_status

from .models import Wallet, Transaction
from .forms import add_user_and_wallet, WalletUpdateForm
from decimal import Decimal  # For handling precise financial calculations
from django.contrib import messages  # Allows sending user-friendly messages
from datetime import datetime, timedelta # For date calculations
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from rest_framework import status

# Create your views here.
def home_page(request):
    return render(request, 'payments/home.html')


# dashboard elements
@login_required(login_url="login")
def dashboard(request):
    user = request.user
    if request.method == 'POST':
        try:
            pending_transactions = Transaction.objects.filter(associated_user=user, state="pending")
            for p_transaction in pending_transactions:
                tx_sig = p_transaction.transaction_signature
                try:
                    result = check_transaction_status(tx_sig)
                    if result:
                        normalized_result = result.lower()
                        match normalized_result:
                            case "processed" | "confirmed" | "finalized":
                                new_status = normalized_result
                            case _:
                                new_status = "pending"
                        if new_status != p_transaction.state:
                            p_transaction.state = new_status
                            p_transaction.save()
                except:
                    break  # Exit early and fall back to GET behavior
        except:
            pass  # Just fall through silently

    all_user_transactions = Transaction.objects.filter(associated_user=user)
    total_value_transacted = 0
    for transaction in all_user_transactions:
        total_value_transacted += transaction.amount
    return render(request, 'payments/dashboard.html', context={
        "transactions": all_user_transactions,
        "total_value_transacted": total_value_transacted
    })

def signup(request):
    if request.method == 'POST':
        form = add_user_and_wallet(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login page after successful signup
    else:
        form = add_user_and_wallet()
    return render(request, 'payments/signup.html', {'form': form})

# user data update
@login_required
def user_settings(request):
    try:
        wallet = request.user.wallet  # Access the wallet via the OneToOneField
    except Wallet.DoesNotExist:
        messages.error(request, "Wallet not found. Please contact support.")
        return redirect('some_fallback_url')  # Replace with your fallback URL

    if request.method == 'POST':
        form = WalletUpdateForm(request.POST, instance=wallet)
        if form.is_valid():
            form.save()
            messages.success(request, "Wallet updated successfully!")
            return redirect('user_settings')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = WalletUpdateForm(instance=wallet)

    return render(request, 'payments/user_settings.html', {'form': form})


# api route to create a new transaction
@api_view(['POST'])
def new_transaction(request):
    payload = request.data
    amount = Decimal(payload.get('amount', "0"))
    transaction_signature = payload.get('transaction_signature', None)
    user_wallet_address = payload.get('user_wallet_address', None)
    if user_wallet_address:
        user_wallet = Wallet.objects.get(wallet_address=user_wallet_address)
        user_id = user_wallet.associated_user.id
        associated_user = User.objects.get(pk=user_id)

        if associated_user:
            new_transaction = Transaction.objects.create(amount=amount,
                                                         transaction_signature=transaction_signature,
                                                         associated_user=associated_user,
                                                         state="pending"
                                                         )
            new_transaction.save()

            return Response({"new_transaction_id": new_transaction.id})

    return Response({"error": "User does not exist."}, status=status.HTTP_400_BAD_REQUEST)



# api route to get a wallet address using a payment token (more secure)

@api_view(['GET'])
def get_wallet_address(request):
    payment_token = request.GET.get('payment_token', None)
    print(payment_token)
    if payment_token:
        wallet_address = Wallet.objects.get(payment_token=payment_token).wallet_address
        print(wallet_address)
        if wallet_address:
            return Response({"wallet_address": wallet_address}, status=status.HTTP_200_OK)
    return Response({"error": "User does not exist."}, status=status.HTTP_400_BAD_REQUEST)