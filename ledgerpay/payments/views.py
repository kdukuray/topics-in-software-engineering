from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Wallet, Transaction
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from decimal import Decimal
from .utils import can_withdraw
from django.utils import timezone
from django.shortcuts import get_object_or_404

# Create your views here.
@login_required(login_url="login")
def dashboard(request):
    all_user_transactions = Transaction.objects.filter(associated_user=request.user)
    return render(request, 'payments/dashboard.html', context={"transactions": all_user_transactions})



@csrf_exempt
@login_required
def withdraw_funds(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST requests allowed'}, status=405)

    try:
        data = json.loads(request.body)
        target_identifier = data.get('target')
        amount = Decimal(data.get('amount'))
    except (KeyError, ValueError, TypeError):
        return JsonResponse({'error': 'Invalid request data'}, status=400)

    sender_wallet = get_object_or_404(Wallet, associated_user=request.user)

    if not can_withdraw(sender_wallet.balance, amount):
        return JsonResponse({'error': 'Insufficient balance or invalid amount'}, status=400)

    try:
        recipient_wallet = Wallet.objects.get(
            payment_token=target_identifier
        ) if "@" not in target_identifier else Wallet.objects.get(
            associated_user__email=target_identifier
        )
    except Wallet.DoesNotExist:
        return JsonResponse({'error': 'Recipient wallet not found'}, status=404)

    # Perform transfer
    sender_wallet.balance -= amount
    recipient_wallet.balance += amount
    sender_wallet.save()
    recipient_wallet.save()

    # Record transaction
    Transaction.objects.create(
        amount=amount,
        transaction_address=recipient_wallet.payment_token,
        associated_user=request.user,
        transaction_date=timezone.now()
    )

    return JsonResponse({
        'message': f'Successfully transferred ${amount} to {recipient_wallet.associated_user.email}'
    }, status=200)