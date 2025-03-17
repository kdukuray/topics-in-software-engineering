from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal



class Wallet(models.Model):
    associated_user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    payment_token = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.associated_user.email}'s Wallet"

    def save(self, *args, **kwargs):
        if self.balance < Decimal("0.00"):
            raise ValueError("Wallet balance cannot be negative")
        super().save(*args, **kwargs)


class Transaction(models.Model):
    transaction_date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_address = models.CharField(max_length=50)
    associated_user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"transaction of ${self.amount} to {self.associated_user.email}"

    def save(self, *args, **kwargs):
        if self.amount <= Decimal("0.00"):
            raise ValueError("Transaction amount must be positive")
        super().save(*args, **kwargs)

