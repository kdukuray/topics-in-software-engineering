from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Wallet, Transaction
from .forms import add_user_and_wallet
import json
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
@login_required(login_url="login")
def payment_method(request):
    wallet, created = Wallet.objects.get_or_create(
        associated_user=request.user,
        defaults={
            'balance': 0.00,
            'payment_token': '121323123',  
            'company_name': request.user.username 
        }
    )
    if request.method == 'POST':
        payment_methods = request.POST.getlist('payment_methods')
        if payment_methods:
            wallet.preferred_payment_methods = payment_methods
            wallet.save()
            return redirect('dashboard')  
        else:
            return render(request, 'payments/payment_method.html', {
                'selected_methods': wallet.preferred_payment_methods,
                'error': 'Please select at least one payment method.'
            })
    return render(request, 'payments/payment_method.html', {
        'selected_methods': wallet.preferred_payment_methods
    })