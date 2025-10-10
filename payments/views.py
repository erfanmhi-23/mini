from rest_framework import generics, permissions
from .models import Payment
from .serializers import PaymentSerializer

class PaymentCreateView(generics.CreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        subscription = serializer.validated_data.get('subscription')
        PLAN_PRICES = {
            'monthly': 100000,
            'quarterly': 270000,
            'semiannual': 500000,
            'yearly': 900000,
        }
        plan = getattr(subscription, 'plan', None)
        amount = PLAN_PRICES.get(plan, 100000)
        serializer.save(user=self.request.user, amount=amount)

class PaymentListView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Payment.objects.filter(user=self.request.user)
