from django.db import models
from django.contrib.auth.models import User



class Wallet(models.Model):
    associated_user = models.OneToOneField(User, on_delete=models.CASCADE,related_name="payments_wallet" )
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    payment_token = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.associated_user.email}'s Wallet"

class Transaction(models.Model):
    transaction_date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_address = models.CharField(max_length=50)
    associated_user = models.ForeignKey(User, on_delete=models.CASCADE,related_name="payments_transactions")

    def __str__(self):
        return f"transaction of ${self.amount} to {self.associated_user.email}"

