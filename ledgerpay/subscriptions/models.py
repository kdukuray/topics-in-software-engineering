import uuid
from django.db import models
from django.contrib.auth.models import User

class Subscription(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    client_name = models.CharField(max_length=255)
    client_email = models.EmailField()
    client_phone = models.CharField(max_length=20, blank=True)

    business = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions')
    plan_name = models.CharField(max_length=255)
    total_price = models.DecimalField(max_digits=10, decimal_places=4)
    interval = models.CharField(max_length=20, choices=[('monthly', 'Monthly'), ('yearly', 'Yearly')])
    status = models.CharField(max_length=20, default='active')

    business_wallet = models.CharField(max_length=255)  # Solana wallet public key

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.plan_name} for {self.client_email}"
