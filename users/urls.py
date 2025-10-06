from django.urls import path
from .views import RegisterUserView, SubscriptionCreateView,RenewSubscriptionView, CancelSubscriptionView,SubscriptionStatusView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('subscription/', SubscriptionCreateView.as_view(), name='create-subscription'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('subscription/renew/', RenewSubscriptionView.as_view(), name='subscription-renew'),
    path('subscription/cancel/', CancelSubscriptionView.as_view(), name='subscription-cancel'),
    path('subscription/status/', SubscriptionStatusView.as_view(), name='subscription-status'),

]
