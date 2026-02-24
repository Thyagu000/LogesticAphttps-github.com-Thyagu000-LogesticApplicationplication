from django.db import models
from core.models import TimeStampedModel
from users.models import User
from tenants.models import Tenant

class DriverProfile(TimeStampedModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    license_number = models.CharField(max_length=100)
    is_available = models.BooleanField(default=False)
    kyc_status = models.CharField(max_length=50)
    rating = models.DecimalField(max_digits=3, decimal_places=2, null=True)


class Vehicle(TimeStampedModel):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    vehicle_number = models.CharField(max_length=50, unique=True)
    vehicle_type = models.CharField(max_length=50)
    capacity_kg = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)


class DriverVehicleAssignment(models.Model):
    driver = models.ForeignKey(DriverProfile, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    assigned_at = models.DateTimeField(auto_now_add=True)
    unassigned_at = models.DateTimeField(null=True, blank=True)