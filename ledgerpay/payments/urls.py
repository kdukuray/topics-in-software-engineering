from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import dashboard, signup, home_page, new_transaction, get_wallet_address, user_settings, generate_payment_link

urlpatterns = [
    path("login/", LoginView.as_view(template_name="payments/login.html"), name="login"),
    path("", dashboard, name="dashboard"),
    path("logout", LogoutView.as_view(), name="logout"),
    path('signup/', signup, name='signup'),
    path('settings/', user_settings, name='user_settings'),
    path("home/", home_page, name="home-page"),  # Define a URL route for withdrawal
    path("new-transaction/", new_transaction, name="new-transaction"),
    path("get-wallet-address/", get_wallet_address, name="get-wallet-address"),
    path("generate-payment-link", generate_payment_link, name="generate-payment-link"),
]