from django.urls import path
from .views import create_subscription, get_subscription, get_business_subscriptions
from . import views
urlpatterns = [
    path('create/', create_subscription),
    path('<uuid:subscription_id>/', get_subscription),
    path('my/', get_business_subscriptions),
    path('dashboard/', views.subscriptions_dashboard, name='subscriptions_dashboard'),  # URL to get subscriptions for business
    path('invoice/<uuid:subscription_id>/', views.send_invoice, name='send_invoice'),

]
