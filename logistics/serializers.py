from rest_framework import serializers
from .models import Item, Receiver, Shipment


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = "__all__"


class ReceiverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Receiver
        fields = "__all__"


class ShipmentSerializer(serializers.ModelSerializer):

    receiver = ReceiverSerializer()

    class Meta:
        model = Shipment
        fields = "__all__"

    def create(self, validated_data):

        receiver_data = validated_data.pop('receiver')
        receiver = Receiver.objects.create(**receiver_data)

        shipment = Shipment.objects.create(
            receiver=receiver,
            **validated_data
        )

        return shipment