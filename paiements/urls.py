from django.urls import path
from .views import PaymentInitializationView, PaymentCompletionView

urlpatterns = [
    path('payment/initialize/', PaymentInitializationView.as_view(), name='payment-initialize'),
    path('payment/complete/<str:reference>/', PaymentCompletionView.as_view(), name='payment-complete'),
]
