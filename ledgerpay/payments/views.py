from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Wallet, Transaction
from .forms import add_user_and_wallet
from .forms import WithdrawalForm  # Import the WithdrawalForm we just created
from decimal import Decimal  # For handling precise financial calculations
from django.contrib import messages  # Allows sending user-friendly messages

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


# Create your views here.
@login_required(login_url="login")
# dashboard elements
def dashboard(request):
    # transactions data
    ## all transactions
    all_user_transactions = Transaction.objects.filter(associated_user=request.user)
    return render(request, 'payments/dashboard.html', context={"transactions": all_user_transactions})


def signup(request):
    if request.method == 'POST':
        form = add_user_and_wallet(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login page after successful signup
    else:
        form = add_user_and_wallet()
    return render(request, 'payments/signup.html', {'form': form})



#Alexandr
# Restrict access to only logged-in users 
@login_required(login_url="login")  
def withdraw_funds(request):
    # Get the wallet of the currently logged-in user
    user_wallet = Wallet.objects.get(associated_user=request.user)

    # Check if the request method is POST 
    if request.method == "POST":
        # Bind form with submitted data
        form = WithdrawalForm(request.POST)  
        # Check if the form data is valid
        if form.is_valid():  
            # Get the withdrawal amount from the form
            amount = form.cleaned_data["amount"]  

            # Check if the user has enough balance
            if amount > user_wallet.balance:
                # Show an error message if balance is too low
                messages.error(request, "Insufficient funds.")  
            else:
                # Deduct the amount from the wallet balance
                user_wallet.balance -= amount  
                # Save the updated wallet balance
                user_wallet.save()  

                # Create a transaction record for tracking withdrawals
                Transaction.objects.create(
                    # Link transaction to the logged-in user
                    associated_user=request.user,  
                    # Store the amount as a negative value (indicating withdrawal)
                    amount=amount, 
                    # Placeholder for transaction address 
                    transaction_address="Withdrawal"  
                )
                # Show a success message
                messages.success(request, "Withdrawal successful!") 
                # Redirect the user back to the dashboard 
                return redirect("dashboard")  

    else:
        # If request is GET, display an empty withdrawal form
        form = WithdrawalForm()  

    # Render the withdrawal page with the form
    #return render(request, "payments/withdraw.html", {"form": form})
    # Render the withdrawal page with the form and current balance
    return render(request, "payments/withdraw.html", {
    "form": form,
    "balance": user_wallet.balance
})



from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
@api_view(['POST'])
def create_transaction(request):
    print(2)
    # print(2)
    payment_token = request.data.get('payment_token')
    amount = Decimal(request.data.get('amount') or 0)
    transaction_address = request.data.get('transaction_address')
    # print(2)
    # Light validation — commented strict checks for demo
    # if not payment_token or not transaction_address or amount <= 0:
    #     return Response({"error": "Invalid input."}, status=status.HTTP_400_BAD_REQUEST)

    # Attempt to find wallet
    wallet = Wallet.objects.get(payment_token=payment_token)
    # try:
    #
    # except Wallet.DoesNotExist:
    #     # For demo, create a wallet if it doesn't exist
    #     wallet = Wallet.objects.create(payment_token=payment_token, balance=Decimal("1000.00"))

    # Skip balance check for demo
    # if wallet.balance < amount:
    #     return Response({"error": "Insufficient balance."}, status=status.HTTP_400_BAD_REQUEST)

    # Deduct balance (or skip this if you want to keep the same balance)
    wallet.balance += amount
    wallet.save()

    # Create transaction
    transaction = Transaction.objects.create(
        amount=amount,
        transaction_address=transaction_address or "DEMO_TXID",
        associated_user=wallet.associated_user
    )
    transaction.save()

    return Response({
        "message": "Transaction created successfully.",
        "transaction_id": transaction.id,
        "new_balance": str(wallet.balance)
    }, status=status.HTTP_201_CREATED)

# except Exception as e:
#     return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
