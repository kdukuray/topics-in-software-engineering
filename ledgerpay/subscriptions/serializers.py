from rest_framework import serializers
from .models import Subscription

class SubscriptionSerializer(serializers.ModelSerializer):
    business_name = serializers.CharField(source='business.username', read_only=True)

    class Meta:
        model = Subscription
        fields = [
            'uuid',
            'client_name',
            'client_email',
            'plan_name',
            'total_price',
            'interval',
            'status',
            'business_wallet',
            'business_name',
        ]
