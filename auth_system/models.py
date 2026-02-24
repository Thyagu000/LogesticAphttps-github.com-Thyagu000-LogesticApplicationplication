from django.db import models
from django.utils import timezone
from users.models import User


class AuthSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    refresh_token = models.TextField()
    expires_at = models.DateTimeField()
    ip_address = models.CharField(max_length=50)
    user_agent = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class OTP(models.Model):
    email = models.EmailField(db_index=True)
    phone = models.CharField(max_length=20, db_index=True, null=True, blank=True)
    otp_code = models.CharField(max_length=6)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)
    attempts = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    used_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['email', 'is_used', 'expires_at']),
            models.Index(fields=['phone', 'is_used', 'expires_at']),
            models.Index(fields=['-created_at']),
        ]

    def mark_used(self):
        self.is_used = True
        self.used_at = timezone.now()
        self.save(update_fields=['is_used', 'used_at'])