from django.contrib import admin
from .models import Tenant, TenantSetting


# Tenant Admin
@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "domain", "is_active", "is_deleted", "created_at")
    search_fields = ("name", "domain", "contact_email")
    list_filter = ("is_active", "is_deleted")
    readonly_fields = ("created_at", "updated_at")

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Only superuser sees all tenants
        if request.user.is_superuser:
            return qs
        # Other admins see only their tenant
        return qs.filter(id=request.user.tenant_id)

# Tenant Setting Admin

@admin.register(TenantSetting)
class TenantSettingAdmin(admin.ModelAdmin):
    list_display = ("id", "tenant", "key", "value", "created_at")
    list_filter = ("tenant", "key")
    search_fields = ("tenant__name", "key")
    readonly_fields = ("created_at",)

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        if request.user.is_superuser:
            return qs

        return qs.filter(tenant=request.user.tenant)

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:
            obj.tenant = request.user.tenant
        super().save_model(request, obj, form, change)

    def has_delete_permission(self, request, obj=None):
        # Prevent deletion of settings
        return False