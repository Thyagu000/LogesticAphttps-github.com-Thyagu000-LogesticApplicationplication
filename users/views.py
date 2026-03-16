from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import User, Role, Permission
from .serializers import TenantUserSerializer, RoleSerializer, PermissionSerializer
from .permissions import IsTenantAdminOrSuperAdmin

# Create your views here.
#TenantUserView
class TenantUserViewSet(ModelViewSet):
    serializer_class = TenantUserSerializer
    permission_classes = [IsAuthenticated, IsTenantAdminOrSuperAdmin]

    def get_queryset(self):
        return User.objects.filter(
            tenant=self.request.user.tenant,
            is_superuser=False
        )

    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        serializer.save()


class PermissionViewSet(ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        # Only Super Admin can create permissions
        if self.request.method in ["POST", "PUT", "PATCH", "DELETE"]:
            if not self.request.user.is_superuser:
                from rest_framework.exceptions import PermissionDenied
                raise PermissionDenied("Only Super Admin can manage permissions.")
        return super().get_permissions()

class PermissionViewSet(ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        # Only Super Admin can create permissions
        if self.request.method in ["POST", "PUT", "PATCH", "DELETE"]:
            if not self.request.user.is_superuser:
                from rest_framework.exceptions import PermissionDenied
                raise PermissionDenied("Only Super Admin can manage permissions.")
        return super().get_permissions()

class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer