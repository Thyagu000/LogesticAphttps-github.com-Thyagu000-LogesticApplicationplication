from django.db import models

class Payment(models.Model):
    shipment_id = models.BigIntegerField()
    payer_id = models.BigIntegerField()
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_method = models.CharField(max_length=50)
    payment_status = models.CharField(max_length=50)
    transaction_reference = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.id} - {self.payment_status}"