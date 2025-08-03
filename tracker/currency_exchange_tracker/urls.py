from django.urls import path
from . import views

app_name = 'currency_exchange'

urlpatterns = [
    path('api/subscribe/', views.subscribe),
    path('api/subscriptions/', views.user_subscriptions),
    path('api/cancel/', views.cancel_subscription),
    path('api/exchange-rate/', views.exchange_rate),
    path('subscribe/', views.subscribe_view, name='subscribe'),
    path('cancel_subscription/', views.cancel_subscription_view, name='cancel_subscription'),
    path('exchange_rate/', views.exchange_rate_view, name='exchange_rate'),
    path('api/exchange-rate-history/', views.exchange_rate_history_api, name='exchange_rate_history_api'),
    path('subscription_list/', views.subscription_list_view, name='subscription_list'),
    path('exchange_rate_list/', views.exchange_rate_list_view, name='exchange_rate_list'),
]
