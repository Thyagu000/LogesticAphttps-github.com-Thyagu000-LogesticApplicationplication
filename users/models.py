from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.core.exceptions import ValidationError
from core.models import TimeStampedModel

# User Manager
class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.full_clean()  # Enforce model validation
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("tenant", None)

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)



# User Model
class User(AbstractBaseUser, PermissionsMixin, TimeStampedModel):

    tenant = models.ForeignKey(
        "tenants.Tenant",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="users"
    )

    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        indexes = [
            models.Index(fields=["email"]),
            models.Index(fields=["tenant"]),
        ]

    # VALIDATION RULES

    def clean(self):
        """
        Enforce enterprise integrity rules:
        - SuperAdmin must NOT belong to a tenant
        - Non-superuser MUST belong to a tenant
        """
        if self.is_superuser and self.tenant is not None:
            raise ValidationError("SuperAdmin cannot belong to a tenant.")

        if not self.is_superuser and self.tenant is None:
            raise ValidationError("Non-superuser must belong to a tenant.")

   
    @property
    def is_super_admin(self):
        return self.is_superuser

    @property
    def is_tenant_admin(self):
        return self.userrole_set.filter(
            role__name="TENANT_ADMIN"
        ).exists()

    @property
    def role_names(self):
        return self.userrole_set.values_list(
            "role__name",
            flat=True
        )

    def __str__(self):
        return self.email



# Role Model
class Role(models.Model):
    tenant = models.ForeignKey(
        "tenants.Tenant",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="roles"
    )

    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("tenant", "name")
        indexes = [
            models.Index(fields=["tenant", "name"]),
        ]

    def __str__(self):
        return f"{self.name} ({self.tenant})"


# Permission Model
class Permission(models.Model):
    code = models.CharField(max_length=100, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.code



# RolePermission Mapping
class RolePermission(models.Model):
    role = models.ForeignKey(
        Role,
        on_delete=models.CASCADE,
        related_name="role_permissions"
    )
    permission = models.ForeignKey(
        Permission,
        on_delete=models.CASCADE,
        related_name="permission_roles"
    )

    class Meta:
        unique_together = ("role", "permission")

    def __str__(self):
        return f"{self.role.name} -> {self.permission.code}"


# ==============================
# UserRole Mapping
class UserRole(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="user_roles"
    )
    role = models.ForeignKey(
        Role,
        on_delete=models.CASCADE,
        related_name="role_users"
    )

    class Meta:
        unique_together = ("user", "role")

    def clean(self):
        """
        Prevent cross-tenant role assignment.
        User and Role must belong to same tenant.
        """
        if self.role.tenant and self.user.tenant != self.role.tenant:
            raise ValidationError(
                "User and Role must belong to the same tenant."
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.email} -> {self.role.name}"