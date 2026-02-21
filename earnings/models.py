from django.db import models
from drivers.models import DriverProfile
from shipments.models import Shipment

class DriverEarning(models.Model):
    driver = models.ForeignKey(DriverProfile, on_delete=models.CASCADE)
    shipment = models.ForeignKey(Shipment, on_delete=models.CASCADE)
    earning_amount = models.DecimalField(max_digits=12, decimal_places=2)
    commission_amount = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)


class Payout(models.Model):
    driver = models.ForeignKey(DriverProfile, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    payout_status = models.CharField(max_length=50)
    processed_at = models.DateTimeField(null=True, blank=True)