from django.db import models
from core.models import TimeStampedModel
from .constants import TENANT_SETTING_CHOICES


class Tenant(TimeStampedModel):
    name = models.CharField(max_length=255)
    domain = models.CharField(max_length=255, unique=True, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)
    contact_email = models.EmailField(max_length=255, unique=True)

    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)  # soft delete support

    class Meta:
        indexes = [
            models.Index(fields=["domain"]),
            models.Index(fields=["slug"]),
        ]

    def __str__(self):
        return self.name

class TenantSetting(models.Model):
    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.CASCADE,
        related_name="settings",
        db_index=True
    )

    key = models.CharField(max_length=100, choices=TENANT_SETTING_CHOICES)
    value = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("tenant", "key")
        indexes = [
            models.Index(fields=["tenant", "key"]),
        ]

    def __str__(self):
        return f"{self.tenant.name} - {self.key}"