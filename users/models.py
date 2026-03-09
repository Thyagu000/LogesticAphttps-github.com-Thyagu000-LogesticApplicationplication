from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from core.models import TimeStampedModel
from tenants.models import Tenant

class User(AbstractBaseUser, PermissionsMixin, TimeStampedModel):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = "email"

    def __str__(self):
        return self.email


class Role(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("tenant", "name")


class Permission(models.Model):
    code = models.CharField(max_length=100, unique=True)
    description = models.TextField()


class RolePermission(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("role", "permission")


class UserRole(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("user", "role")