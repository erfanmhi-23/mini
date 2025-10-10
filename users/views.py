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
        subscription = Subscription.objects.filter(user=request.user).order_by('-start_date').first()

        if not subscription:
            return Response({"detail": "No subscription found for user."}, status=status.HTTP_404_NOT_FOUND)

        days = Subscription.PLAN_DURATIONS.get(subscription.plan, 30)
        if subscription.active and subscription.end_date >= today:
            return Response({
                "detail": "You already have an active subscription.",
                "plan": subscription.plan,
                "end_date": subscription.end_date
            })
        subscription.end_date = today + timedelta(days=days)
        subscription.active = True
        subscription.save()
        return Response({
            "detail": "Subscription renewed successfully.",
            "plan": subscription.plan,
            "new_end_date": subscription.end_date
        })

class CancelSubscriptionView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        today = timezone.localdate()
        subscription = Subscription.objects.filter(user=request.user).order_by('-start_date').first()

        if not subscription:
            return Response({"detail": "No subscription found for user."}, status=status.HTTP_404_NOT_FOUND)

        if not subscription.active or subscription.end_date < today:
            return Response({"detail": "No active subscription to cancel."}, status=status.HTTP_400_BAD_REQUEST)

        subscription.active = False
        subscription.end_date = today
        subscription.save()
        return Response({"detail": "Subscription cancelled successfully."})


class SubscriptionStatusView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        today = timezone.localdate()
        subscription = Subscription.objects.filter(user=request.user).order_by('-start_date').first()

        if not subscription:
            return Response({"detail": "No subscription found for user."}, status=status.HTTP_404_NOT_FOUND)

        status_text = "active" if (subscription.active and subscription.end_date >= today) else "inactive"
        days_left = max((subscription.end_date - today).days, 0)
        return Response({
            "plan": subscription.plan,
            "end_date": subscription.end_date,
            "active": subscription.active,
            "status": status_text,
            "days_left": days_left
        })