import uuid
from django.db import models
from django.contrib.auth.models import User


class Notification(models.Model):

    class NotificationType(models.TextChoices):
        SHIPMENT_ASSIGNED = "SHIPMENT_ASSIGNED", "Shipment Assigned"
        DELIVERY_UPDATE = "DELIVERY_UPDATE", "Delivery Status Update"
        PAYMENT_RECEIVED = "PAYMENT_RECEIVED", "Payment Received"
        PAYOUT_PROCESSED = "PAYOUT_PROCESSED", "Payout Processed"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="notifications"
    )

    title = models.CharField(max_length=255)
    message = models.TextField()

    type = models.CharField(
        max_length=50,
        choices=NotificationType.choices
    )

    reference_id = models.UUIDField(null=True, blank=True)

    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title