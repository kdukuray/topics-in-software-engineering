#Alex
from django import forms

class WithdrawalForm(forms.Form):
    wallet_address = forms.CharField(
        max_length=100, 
        required=True, 
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    amount = forms.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        required=True, 
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
