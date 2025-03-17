from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import dashboard
from . import views

urlpatterns = [
    path("login/", LoginView.as_view(template_name="withdrawal/login.html"), name="login"),
    path("", dashboard, name="dashboard"),
    path("logout", LogoutView.as_view(), name="logout"),
    path("withdrawal/", views.withdrawal_request, name="withdrawal_request"),
    path("owner-dashboard/", views.owner_dashboard, name="owner_dashboard"),
    path("process_withdrawals/", views.process_pending_withdrawals, name="process_withdrawals"),
    path("dashboard/", dashboard, name="dashboard"),

]