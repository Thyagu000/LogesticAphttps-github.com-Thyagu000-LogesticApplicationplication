from django.db import models


class Shipment(TimeStampedModel):

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

    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    driver = models.ForeignKey(
        DriverProfile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    order_number = models.CharField(max_length=100, unique=True)
    tracking_number = models.CharField(
        max_length=50,
        unique=True,
        null=True,
        blank=True
    )

    sender_name = models.CharField(max_length=100, null=True, blank=True)
    receiver_name = models.CharField(max_length=100, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    pickup_address = models.TextField(null=True, blank=True)
    delivery_address = models.TextField(null=True, blank=True)
    total_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default="Created"
    )

    is_cod = models.BooleanField(default=False)
    is_reverse = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.order_number


class Parcel(models.Model):
    shipment = models.ForeignKey(Shipment, on_delete=models.CASCADE)
    weight_kg = models.DecimalField(max_digits=10, decimal_places=2)
    length_cm = models.DecimalField(max_digits=10, decimal_places=2)
    width_cm = models.DecimalField(max_digits=10, decimal_places=2)
    height_cm = models.DecimalField(max_digits=10, decimal_places=2)
    declared_value = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.tracking_number
