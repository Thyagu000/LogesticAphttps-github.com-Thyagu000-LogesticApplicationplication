from django.db.models.signals import post_save
from django.dispatch import receiver
from shipments.models import Shipment
from .services import claculate_driver_earning


@receiver(post_save, sender=Shipment)
def create_earning_when_delivered(sender, instance, created, **kwargs):

    if not created and instance.status == 'DELIVERED':
        claculate_driver_earning(instance)
