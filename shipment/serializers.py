from rest_framework import serializers
from .models import Shipment, Parcel

class ParcelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parcel
        fields = ['id', 'weight', 'description']

class ShipmentSerializer(serializers.ModelSerializer):
    parcels = ParcelSerializer(many=True)

    class Meta:
        model = Shipment
        fields = ['id', 'shipment_code', 'parcels']

    def create(self, validated_data):
        parcels_data = validated_data.pop('parcels')
        if len(parcels_data) < 1:
            raise serializers.ValidationError("At least one parcel is required.")
        shipment = Shipment.objects.create(**validated_data)
        for parcel_data in parcels_data:
            Parcel.objects.create(shipment=shipment, **parcel_data)
        return shipment

    def update(self, instance, validated_data):
        parcels_data = validated_data.pop('parcels', None)
        instance.shipment_code = validated_data.get('shipment_code', instance.shipment_code)
        instance.save()
        if parcels_data:
            instance.parcels.all().delete()
            for parcel_data in parcels_data:
                Parcel.objects.create(shipment=instance, **parcel_data)
        return instance