from django.urls import path
from .views import PaymentCreateView, PaymentListView

urlpatterns = [
    path('create/', PaymentCreateView.as_view(), name='payment-create'),
    path('my/', PaymentListView.as_view(), name='payment-list'),
]
