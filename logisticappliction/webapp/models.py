from django.db import models

# Create your models here.

class Webhook(models.Model):

    EVENT_CHOICES = [
        ('shipment_status_changed', 'Shipment Status Changed'),
        ('payment_update', 'Payment Update'),
        ('payout_processed', 'Payout Processed'),
    ]

    webhook_url = models.URLField()
    event = models.CharField(max_length=100, choices=EVENT_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.webhook_url


class WebhookLog(models.Model):

    webhook = models.ForeignKey(Webhook, on_delete=models.CASCADE)
    status = models.CharField(max_length=20)
    response = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)