from django.db import models
class Webhook(models.Model):
    tenant = models.ForeignKey("tenants.Tenant", on_delete=models.CASCADE)
    url = models.TextField()
    secret = models.CharField(max_length=255)
    event_type = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)


class WebhookLog(models.Model):
    webhook = models.ForeignKey(Webhook, on_delete=models.CASCADE)
    payload = models.JSONField()
    response_status = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)