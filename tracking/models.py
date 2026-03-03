from django.db import models
from django.contrib.auth import get_user_model
from shipments.models import Shipment
from django.utils import timezone

User = get_user_model()


class TrackingLog(models.Model):
    """
    Records every status change of a shipment for tracking purposes.
    """
    shipment = models.ForeignKey(
        Shipment, on_delete=models.CASCADE, related_name='tracking_logs'
    )
    status = models.CharField(max_length=100)
    updated_by = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL
    )
    notes = models.TextField(blank=True)
    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"{self.shipment} - {self.status} at {self.timestamp}"


class DeliveryAttempt(models.Model):
    """
    Records each delivery attempt for a shipment, including reason for failure,
    optional proof image/signature, and RTO marking if max attempts reached.
    """
    shipment = models.ForeignKey(
        Shipment, on_delete=models.CASCADE, related_name='delivery_attempts'
    )
    attempt_number = models.PositiveIntegerField()
    attempted_by = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL
    )
    reason = models.TextField()
    proof_image = models.ImageField(
        upload_to='delivery_proofs/', null=True, blank=True
    )
    timestamp = models.DateTimeField(default=timezone.now)
    is_rto = models.BooleanField(default=False)
    geo_location = models.CharField(
        max_length=255, blank=True, null=True
    )  # placeholder for future geolocation

    class Meta:
        unique_together = ('shipment', 'attempt_number')
        ordering = ['attempt_number']

    def __str__(self):
        return f"Attempt {self.attempt_number} for {self.shipment}"


# Utility functions to enforce business rules

MAX_ATTEMPTS = 3  # Configurable max delivery attempts


def update_shipment_status(shipment, status, user=None, notes=""):
    """
    Creates a tracking log and updates the shipment status.
    """
    TrackingLog.objects.create(
        shipment=shipment,
        status=status,
        updated_by=user,
        notes=notes
    )
    shipment.status = status
    shipment.save()


def record_delivery_attempt(shipment, reason, user=None, proof_image=None):
    """
    Records a delivery attempt and marks RTO if max attempts reached.
    """
    attempt_number = shipment.delivery_attempts.count() + 1
    is_rto = attempt_number >= MAX_ATTEMPTS
    attempt = DeliveryAttempt.objects.create(
        shipment=shipment,
        attempt_number=attempt_number,
        attempted_by=user,
        reason=reason,
        proof_image=proof_image,
        is_rto=is_rto
    )
    if is_rto:
        update_shipment_status(shipment, "RTO", user)
    else:
        update_shipment_status(shipment, "Delivery Attempted", user)
    return attempt