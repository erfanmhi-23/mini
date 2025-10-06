from rest_framework import serializers
from .models import Payment

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ('id', 'user', 'subscription', 'amount', 'date', 'status')
        read_only_fields = ('date',)
