from rest_framework import serializers
from .models import Shipment

class ShipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shipment
        fields = [
            'id',
            'tracking_number',
            'sender_name',
            'receiver_name',
            'address',
            'status',
            'is_reverse',
            'created_at',
            'updated_at'
        ]