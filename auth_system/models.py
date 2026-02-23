from django.db import models
from users.models import User

class AuthSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    refresh_token = models.TextField()
    expires_at = models.DateTimeField()
    ip_address = models.CharField(max_length=50)
    user_agent = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)