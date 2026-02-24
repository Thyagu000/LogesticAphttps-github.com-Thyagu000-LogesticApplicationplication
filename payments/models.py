from django.db import models
from shipments.models import Shipment
from users.models import User

class Payment(models.Model):
    shipment = models.ForeignKey(Shipment, on_delete=models.CASCADE)
    payer = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_method = models.CharField(max_length=50)
    payment_status = models.CharField(max_length=50)
    transaction_reference = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)


class Refund(models.Model):
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
    refund_amount = models.DecimalField(max_digits=12, decimal_places=2)
    reason = models.TextField()
    status = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)