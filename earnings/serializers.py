from rest_framework import serializers
from .models import DriverEarning, Payout

class DriverEarningSerializer(serializers.ModelSerializer):
    shipment_id = serializers.IntegerField(source = 'shipment.id')
    
    class Meta:
        model = DriverEarning
        fields = [
            'id',
            'shipment_id',
            'earning_amount',
            'commission_amount',
            'is_paid',
            'created_at'
        ]
        
class PayoutSerializer(serializers.ModelSerializer):
    earnings = DriverEarningSerializer(many = True, read_only= True)
    
    class Meta:
        model = Payout
        fields = [
            'id',
            'driver',
            'total_amount',
            'payout_status',
            'reference_id',
            'created_at',
            'processed_at',
            'earnings'
        ]