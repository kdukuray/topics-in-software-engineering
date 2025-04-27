from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
<<<<<<< HEAD
from .views import dashboard, signup, payment_method
=======
from .views import dashboard, signup
from .views import withdraw_funds  # Import the new withdrawal function
>>>>>>> 04493b24a875b60e443abb6a1a46403b03d27bf3

urlpatterns = [
    path("login/", LoginView.as_view(template_name="payments/login.html"), name="login"),
    path("", dashboard, name="dashboard"),
    path("logout", LogoutView.as_view(), name="logout"),
    path('signup/', signup, name='signup'),
<<<<<<< HEAD
    path('payment/', payment_method, name='payment_method'),
=======
    path("withdraw/", withdraw_funds, name="withdraw"),  # Define a URL route for withdrawal
>>>>>>> 04493b24a875b60e443abb6a1a46403b03d27bf3
]