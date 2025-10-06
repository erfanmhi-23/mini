from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, generics
from django.utils import timezone
from .models import CustomUser, Subscription
from .serializers import RegisterUserSerializer, SubscriptionSerializer
from datetime import timedelta

class RegisterUserView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterUserSerializer
    permission_classes = [permissions.AllowAny]

class SubscriptionCreateView(generics.CreateAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated]

class RenewSubscriptionView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        today = timezone.localdate()
        subscription = Subscription.objects.filter(
            user=request.user,
            end_date__gte=today
        ).order_by('-start_date').first()

        if not subscription:
            return Response({"detail": "No active subscription found."}, status=status.HTTP_404_NOT_FOUND)

        PLAN_DURATIONS = {
            'monthly': 30,
            'quarterly': 90,
            'semiannual': 180,
            'yearly': 365
        }
        days = PLAN_DURATIONS.get(subscription.plan, 30)

        if subscription.end_date < today:
            subscription.end_date = today + timedelta(days=days)
            subscription.active = True
        else:
            subscription.end_date += timedelta(days=days)

        subscription.save()
        return Response({
            "detail": "Subscription renewed successfully.",
            "plan": subscription.plan,
            "new_end_date": subscription.end_date
        }, status=status.HTTP_200_OK)

class CancelSubscriptionView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        today = timezone.localdate()
        subscription = Subscription.objects.filter(
            user=request.user,
            end_date__gte=today
        ).order_by('-start_date').first()

        if not subscription:
            return Response({"detail": "No active subscription to cancel."}, status=status.HTTP_404_NOT_FOUND)

        subscription.active = False
        subscription.end_date = today
        subscription.save()
        return Response({"detail": "Subscription cancelled successfully."}, status=status.HTTP_200_OK)

class SubscriptionStatusView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        today = timezone.localdate()
        subscription = Subscription.objects.filter(
            user=request.user,
            end_date__gte=today
        ).order_by('-start_date').first()

        if not subscription:
            return Response({"detail": "No active subscription found."}, status=status.HTTP_404_NOT_FOUND)

        days_left = (subscription.end_date - today).days
        return Response({
            "plan": subscription.plan,
            "end_date": subscription.end_date,
            "active": subscription.active,
            "days_left": days_left
        }, status=status.HTTP_200_OK)
