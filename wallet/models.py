from django.db import models
from users.models import User

class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=14, decimal_places=2)
    updated_at = models.DateTimeField(auto_now=True)


class WalletTransaction(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    type = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    reference_id = models.BigIntegerField(null=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)