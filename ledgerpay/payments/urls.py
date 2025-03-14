from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import dashboard

urlpatterns = [
    path("login/", LoginView.as_view(template_name="payments/login.html"), name="login"),
    path("dashboard/", dashboard, name="dashboard"),
]