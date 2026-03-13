from django.db import models
from core.models import TimeStampedModel

class Tenant(TimeStampedModel):
    name = models.CharField(max_length=255)
    domain = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class TenantSetting(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    key = models.CharField(max_length=100)
    value = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("tenant", "key")