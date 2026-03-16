from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import ShipmentTracking
from shipments.models import Shipment

@receiver(post_save, sender=Shipment)
def auto_tracking_log(sender, instance, **kwargs):
    # Automatically create a tracking log on shipment status change
    ShipmentTracking.objects.create(
        shipment=instance,
        status=instance.current_status,
        remarks="Auto log",
    )