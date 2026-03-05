from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import Tenant, TenantSetting
from .serializers import TenantSerializer, TenantSettingSerializer

# 1. Custom Permission for Super Admin
class IsSuperAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.is_superuser
        )
class TenantViewSet(viewsets.ModelViewSet):
    queryset = Tenant.objects.filter(is_deleted=False)
    serializer_class = TenantSerializer
    permission_classes = [IsSuperAdmin]

    def perform_destroy(self, instance):
        # Soft delete instead of hard delete
        instance.is_deleted = True
        instance.is_active = False
        instance.save()

class TenantSettingViewSet(viewsets.ModelViewSet):
    serializer_class = TenantSettingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)

        if not request.user.tenant.is_active:
            raise permissions.PermissionDenied(
                "Your tenant is inactive. Contact support."
            )

    def get_queryset(self):
        return TenantSetting.objects.filter(
            tenant=self.request.user.tenant
        )

    def get_object(self):
        obj = super().get_object()

        # Prevent cross-tenant access
        if obj.tenant != self.request.user.tenant:
            raise permissions.PermissionDenied(
                "You do not have permission to access this resource."
            )
        return obj

    def perform_create(self, serializer):
        serializer.save(tenant=self.request.user.tenant)

    def perform_update(self, serializer):
        serializer.save(tenant=self.request.user.tenant)

    def destroy(self, request, *args, **kwargs):
        return Response(
            {"detail": "Deletion of tenant settings is not allowed. Please update values instead."},
            status=status.HTTP_403_FORBIDDEN
        )