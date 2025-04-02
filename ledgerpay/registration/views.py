'''
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django import forms
from django.contrib.auth.hashers import make_password
from registration.models import BusinessOwner  # Import the BusinessOwner model

# Create the registration form class
class RegistrationForm(forms.Form):
    name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

# View to handle registration
def register_business_owner(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # Extract the form data
            name = form.cleaned_data["name"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            # Hash the password for security
            hashed_password = make_password(password)

            # Create and save the BusinessOwner object to the database
            business_owner = BusinessOwner(name=name, email=email, password=hashed_password)
            business_owner.save()

            # Redirect to a success page or return a success message
            return HttpResponse("Registration successful!")
            # Or you can redirect to a different view, like a dashboard
            # return redirect('dashboard') # Make sure you have a URL for the dashboard
    else:
        form = RegistrationForm()

    return render(request, "registration/register.html", {"form": form})
'''
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django import forms
from django.contrib.auth.hashers import make_password
from registration.models import BusinessOwner
from django.db.utils import IntegrityError

# Create the registration form class
class RegistrationForm(forms.Form):
    name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

# View to handle registration
def register_business_owner(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # Extract the form data
            name = form.cleaned_data["name"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            # Check if email already exists
            if BusinessOwner.objects.filter(email=email).exists():
                # Returning HTML with error message
                return render(request, "registration/register.html", {
                    "form": form, 
                    "error_message": "Email already exists"
                })

            # Hash the password for security
            hashed_password = make_password(password)

            # Create and save the BusinessOwner object to the database
            try:
                business_owner = BusinessOwner(name=name, email=email, password=hashed_password)
                business_owner.save()
            except IntegrityError:
                return HttpResponse("Error saving data", status=500)

            # Return success response
            return HttpResponse("Registration successful!")
    else:
        form = RegistrationForm()

    return render(request, "registration/register.html", {"form": form})
