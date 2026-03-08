from django.db import models

class Shipment(models.Model):

    STATUS_CHOICES = [
        ("created","Created"),
        ("assigned","Assigned"),
        ("picked_up","Picked Up"),
        ("in_transit","In Transit"),
        ("delivered","Delivered"),
    ]

    order_id = models.CharField(max_length=100)
    customer_name = models.CharField(max_length=200)

    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    status = models.CharField(max_length=50, choices=STATUS_CHOICES)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.order_id
