from django.db import models
from django.contrib.auth.models import User


class Item(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class Receiver(models.Model):
    name = models.CharField(max_length=200)
    contact_number = models.CharField(max_length=15)
    delivery_address = models.TextField()

    def __str__(self):
        return self.name


class Shipment(models.Model):

    STATUS_CHOICES = [
        ('PENDING','Pending'),
        ('IN_TRANSIT','In Transit'),
        ('DELIVERED','Delivered'),
    ]

    user = models.ForeignKey(User,on_delete=models.CASCADE)
    item = models.ForeignKey(Item,on_delete=models.CASCADE)
    receiver = models.ForeignKey(Receiver,on_delete=models.CASCADE)

    payment_status = models.BooleanField(default=False)

    delivery_status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDING'
    )

    delivery_location = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Shipment {self.id}"
