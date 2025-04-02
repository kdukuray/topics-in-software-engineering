from django import forms
from django.core.exceptions import ValidationError
import re

# A password validator function for basic strength check
def validate_password(value):
    if len(value) < 8:
        raise ValidationError('Password must be at least 8 characters long.')
    if not re.search(r'[A-Z]', value):
        raise ValidationError('Password must contain at least one uppercase letter.')
    if not re.search(r'[0-9]', value):
        raise ValidationError('Password must contain at least one number.')

class BusinessOwnerRegistrationForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()  # No additional validation for email
    password = forms.CharField(widget=forms.PasswordInput, validators=[validate_password])
