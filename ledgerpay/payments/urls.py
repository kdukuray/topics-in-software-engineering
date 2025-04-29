from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import dashboard, signup, payment_method

urlpatterns = [
    path("login/", LoginView.as_view(template_name="payments/login.html"), name="login"),
    path("", dashboard, name="dashboard"),
    path("logout", LogoutView.as_view(), name="logout"),
    path('signup/', signup, name='signup'),
    path('payment/', payment_method, name='payment_method'),
]