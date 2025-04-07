from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import dashboard, signup
from .views import withdraw_funds  # Import the new withdrawal function

urlpatterns = [
    path("login/", LoginView.as_view(template_name="payments/login.html"), name="login"),
    path("", dashboard, name="dashboard"),
    path("logout", LogoutView.as_view(), name="logout"),
    path('signup/', signup, name='signup'),
    path("withdraw/", withdraw_funds, name="withdraw"),  # Define a URL route for withdrawal
]