from rest_framework import serializers
from .models import Shipment


class ShipmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Shipment
        fields = [
            "id",
            "order_number",
            "tracking_number",
            "sender_name",
            "receiver_name",
            "address",
            "pickup_address",
            "delivery_address",
            "status",
            "total_price",
            "is_cod",
            "is_reverse",
            "is_deleted",
            "tenant",
            "created_at",
            "updated_at",
        ]

        read_only_fields = (
            "id",
            "tenant",
            "created_at",
            "updated_at",
        )