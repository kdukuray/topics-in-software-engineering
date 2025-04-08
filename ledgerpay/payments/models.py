from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal

class Wallet(models.Model):
    # Username from the users table
    associated_user = models.OneToOneField(User, on_delete=models.CASCADE)
    # A company name column for future use of transaction making pages
    company_name = models.CharField(max_length=255, blank=True, null=True)
    # the user balance with us
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    # possibly public key of user crypto wallet
    payment_token = models.CharField(max_length=50)
    # a display of the object or row
    def __str__(self):
        return f"{self.company_name}'s Wallet"

    def save(self, *args, **kwargs):
        if self.balance < Decimal("0.00"):
            raise ValueError("Wallet balance cannot be negative")
        if not self.company_name:
            # could be a diffrent default
            self.company_name = "Not spacified"
        super().save(*args, **kwargs)


class Transaction(models.Model):
    # states of transactions
    class TransactionState(models.TextChoices):
        PENDING = 'pending', 'Pending'
        PROCESSING = 'processing', 'Processing'
        COMPLETED = 'completed', 'Completed'
        FAILED = 'failed', 'Failed'
        CANCELED = 'canceled', 'Canceled'

    # date transaction was made
    transaction_date = models.DateTimeField(auto_now_add=True)
    # amout of money
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    # blockchain address to confirm the transaction
    transaction_address = models.CharField(max_length=50)
    # the user who got paid
    associated_user = models.ForeignKey(User, on_delete=models.CASCADE)
    # Currentstate of the transaction, made for dashboard filtering, need confirmation before migration
    state = models.CharField(
        max_length=10,
        choices=TransactionState.choices,
        default=TransactionState.PENDING
    )

    # a display of the object or row
    def __str__(self):
        return f"transaction of ${self.amount} to {self.associated_user.email}, state: {self.get_state_display()}"

    def save(self, *args, **kwargs):
        if self.amount <= Decimal("0.00"):
            raise ValueError("Transaction amount must be positive")
        super().save(*args, **kwargs)


    def set_state(self, new_state):
        """Helper method to change the state of a transaction."""
        if new_state in [state[0] for state in self.TransactionState.choices]:
            self.state = new_state
            self.save()

