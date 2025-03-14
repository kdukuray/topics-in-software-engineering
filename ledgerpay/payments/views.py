from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Wallet, Transaction

# Create your views here.
@login_required(login_url="login")
def dashboard(request):
    all_user_transactions = Transaction.objects.filter(associated_user=request.user)
    return render(request, 'payments/dashboard.html', context={"transactions": all_user_transactions})