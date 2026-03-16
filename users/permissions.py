from rest_framework.permissions import BasePermission


class IsTenantAdminOrSuperAdmin(BasePermission):

    def has_permission(self, request, view):
        user = request.user

        if not user or not user.is_authenticated:
            return False

        if user.is_superuser:
            return True

        return user.user_roles.filter(
            role__name="TENANT_ADMIN"
        ).exists()



