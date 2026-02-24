from django.db import models
from shipments.models import Shipment

class ShipmentTracking(models.Model):
    shipment = models.ForeignKey(Shipment, on_delete=models.CASCADE)
    status = models.CharField(max_length=50)
    location = models.TextField()
    latitude = models.DecimalField(max_digits=10, decimal_places=7)
    longitude = models.DecimalField(max_digits=10, decimal_places=7)
    remarks = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class DeliveryAttempt(models.Model):
    shipment = models.ForeignKey(Shipment, on_delete=models.CASCADE)
    attempt_number = models.IntegerField()
    status = models.CharField(max_length=50)
    remarks = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)