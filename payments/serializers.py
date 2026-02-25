from rest_framework import serializers
from .models import Payment

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            'id',
            'shipment_id',
            'payer_id',
            'amount',
            'payment_method',
            'payment_status',
            'transaction_reference',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']