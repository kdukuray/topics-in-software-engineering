from django.db import models
from django.contrib.auth.models import User



class Wallet(models.Model):
    associated_user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="withdrawal_wallet")
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    payment_token = models.CharField(max_length=50,default="default_token")

    def __str__(self):
        return f"{self.associated_user.email}'s Wallet"

class Transaction(models.Model):
    transaction_date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_address = models.CharField(max_length=50)
    associated_user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"transaction of ${self.amount} to {self.associated_user.email}"

# Alex Model for Withdrawals
class WithdrawalRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    associated_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="withdrawal_transactions")
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    wallet_address = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Withdrawal of ${self.amount} by {self.associated_user.email} - {self.status}"