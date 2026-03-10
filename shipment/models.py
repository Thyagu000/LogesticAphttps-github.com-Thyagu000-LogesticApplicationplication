from django.db import models
from django.core.exceptions import ValidationError

from django.db import models

class Shipment(models.Model):
    shipment_code = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.shipment_code


class Parcel(models.Model):
    shipment = models.ForeignKey(Shipment, on_delete=models.CASCADE, related_name='parcels')
    weight = models.FloatField()
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Parcel of {self.shipment.shipment_code} - {self.weight}kg"