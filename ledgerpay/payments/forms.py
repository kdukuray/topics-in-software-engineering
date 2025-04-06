# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Wallet
from decimal import Decimal

class add_user_and_wallet(UserCreationForm):

    company_name = forms.CharField(max_length=255, required=True)
    payment_token = forms.CharField(max_length=50, required=True)

    class Meta:
        model = User
        fields = ('username','email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        
        wallet = Wallet(associated_user=user, company_name=self.cleaned_data['company_name'],balance = Decimal("0.00"), payment_token=self.cleaned_data['payment_token'])
        wallet.save()
        return user
    
    # testUser4
    # testEmail4@gmail.com
    # password4Test
    # company name 4 test
    # tokenest4