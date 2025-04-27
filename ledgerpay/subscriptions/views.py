from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Subscription
from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import Subscription
from .serializers import SubscriptionSerializer
'''
@api_view(['POST'])
def create_subscription(request):
    data = request.data
    business_name = data.get("business_name")

    try:
        business = User.objects.get(username=business_name)
    except User.DoesNotExist:
        return Response({"error": "Business not found."}, status=404)

    subscription = Subscription.objects.create(
        client_name=data["client_name"],
        client_email=data["client_email"],
        client_phone=data.get("client_phone", ""),
        plan_name=data["plan_name"],
        total_price=data["total_price"],
        interval="monthly",  # temporary default
        status="active",
        business_wallet="5hM386Bx7DeyWTP3VvePE5TAYTxMU4s9jvSWQcPbhuE7",  # update to actual wallet later
        business=business
    )

    return Response({"message": "Subscription created", "subscription_id": subscription.uuid}, status=201)
'''

from payments.models import Wallet  # make sure to import your Wallet model

@api_view(['POST'])
def create_subscription(request):
    data = request.data
    business_name = data.get("business_name")

    try:
        business = User.objects.get(username=business_name)
    except User.DoesNotExist:
        return Response({"error": "Business not found."}, status=404)

    try:
        wallet = business.wallet  # Assuming OneToOneField from User to Wallet
    except Wallet.DoesNotExist:
        return Response({"error": "Wallet for this business not found."}, status=404)

    subscription = Subscription.objects.create(
        client_name=data["client_name"],
        client_email=data["client_email"],
        client_phone=data.get("client_phone", ""),
        plan_name=data["plan_name"],
        total_price=data["total_price"],
        interval="monthly",  # or let user choose later
        status="active",
        business_wallet=wallet.payment_token,  # ✅ Use the actual wallet token dynamically
        business=business
    )

    return Response({"message": "Subscription created", "subscription_id": subscription.uuid}, status=201)



@api_view(['GET'])
def get_subscription(request, subscription_id):
    try:
        subscription = Subscription.objects.get(uuid=subscription_id)
        serializer = SubscriptionSerializer(subscription)
        return Response(serializer.data)
    except Subscription.DoesNotExist:
        return Response({'error': 'Subscription not found'}, status=404)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_business_subscriptions(request):
    subscriptions = Subscription.objects.filter(business=request.user)
    serializer = SubscriptionSerializer(subscriptions, many=True)
    return Response(serializer.data)



# subscriptions/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import Subscription

@login_required
def subscriptions_dashboard(request):
    # Get the logged-in user's wallet and use the 'payment_token' field
    business_wallet = request.user.wallet.payment_token  # Use payment_token if it’s the correct identifier

    # Fetch subscriptions that match the business_wallet
    subscriptions = Subscription.objects.filter(business_wallet=business_wallet)

    # Render the subscriptions dashboard page
    return render(request, 'subscriptions_dashboard.html', {
        'subscriptions': subscriptions,
    })




@csrf_exempt
def send_invoice(request, subscription_id):
    if request.method == 'POST':
        subscription = get_object_or_404(Subscription, uuid=subscription_id)

        # Just simulate sending an invoice
        print(f"Sending invoice to {subscription.client_email} for {subscription.plan_name} at ${subscription.total_price}")

        return redirect('subscriptions_dashboard')
