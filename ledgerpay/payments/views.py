from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Wallet, Transaction
from .forms import add_user_and_wallet

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