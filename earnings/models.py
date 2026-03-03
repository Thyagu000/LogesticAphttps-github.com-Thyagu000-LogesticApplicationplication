from django.db import models
from drivers.models import DriverProfile
from shipments.models import Shipment

class DriverEarning(models.Model):
    driver = models.ForeignKey(DriverProfile, on_delete=models.CASCADE, related_name='earnings')
    shipment = models.ForeignKey(Shipment, on_delete=models.CASCADE,related_name='earnings')
    earning_amount = models.DecimalField(max_digits=12, decimal_places=2)
    commission_amount = models.DecimalField(max_digits=12, decimal_places=2)
    payout = models.ForeignKey('Payout',null=True, blank=True, on_delete=models.SET_NULL, related_name='earnings')
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Earning {self.driver} - {self.earning_amount}"


class Payout(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('PROCESSING', 'Processing'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
    )
    driver = models.ForeignKey(DriverProfile, on_delete=models.CASCADE, related_name='payouts')
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    payout_status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='PENDING')
    refernce_id = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"Payout #{self.id} - {self.driver}"
