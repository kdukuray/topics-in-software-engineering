from django.urls import path
from . import views

urlpatterns = [
    path('', views.register_business_owner, name='register'),  # This should handle the GET request for the registration page
]
