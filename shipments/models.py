from django.db import models


class Shipment(models.Model):

    STATUS_CHOICES = [
        ("Created", "Created"),
        ("Assigned", "Assigned"),
        ("Picked Up", "Picked Up"),
        ("In Transit", "In Transit"),
        ("Out for Delivery", "Out for Delivery"),
        ("Delivered", "Delivered"),
        ("Cancelled", "Cancelled"),
        ("RTO", "RTO"),
        ("Delivery Failed", "Delivery Failed"),
    ]

    tracking_number = models.CharField(max_length=50, unique=True)
    sender_name = models.CharField(max_length=100)
    receiver_name = models.CharField(max_length=100)
    address = models.TextField()

    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default="Created")

    is_reverse = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.tracking_number