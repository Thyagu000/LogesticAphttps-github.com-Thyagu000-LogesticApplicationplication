from django.db import models
from core.models import TimeStampedModel
from tenants.models import Tenant
from users.models import User
from drivers.models import DriverProfile

class Shipment(TimeStampedModel):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    driver = models.ForeignKey(DriverProfile, on_delete=models.SET_NULL, null=True)

    order_number = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=50)
    pickup_address = models.TextField()
    delivery_address = models.TextField()
    total_price = models.DecimalField(max_digits=12, decimal_places=2)

    is_cod = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)


class Parcel(models.Model):
    shipment = models.ForeignKey(Shipment, on_delete=models.CASCADE)
    weight_kg = models.DecimalField(max_digits=10, decimal_places=2)
    length_cm = models.DecimalField(max_digits=10, decimal_places=2)
    width_cm = models.DecimalField(max_digits=10, decimal_places=2)
    height_cm = models.DecimalField(max_digits=10, decimal_places=2)
    declared_value = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)