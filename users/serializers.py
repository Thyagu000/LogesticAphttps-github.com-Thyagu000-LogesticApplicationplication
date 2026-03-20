from rest_framework import serializers
from .models import User, Role, UserRole
from .models import Permission, Role, RolePermission


class TenantUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        min_length=6
    )

    roles = serializers.ListField(
        child=serializers.CharField(),
        write_only=True,
        required=False
    )

    tenant = serializers.IntegerField(
        write_only=True,
        required=False
    )

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "phone",
            "is_active",
            "password",
            "roles",
            "tenant",
        ]
        read_only_fields = ["id"]

    def create(self, validated_data):
        roles_data = validated_data.pop("roles", [])
        password = validated_data.pop("password")
        email = validated_data.pop("email")

    # Remove tenant from validated_data to avoid duplication
        validated_data.pop("tenant", None)

        request_user = self.context["request"].user

    # Super Admin Flow
        if request_user.is_superuser:
            tenant_id = self.initial_data.get("tenant")

            if not tenant_id:
                raise serializers.ValidationError(
                {"tenant": "Tenant ID is required when Super Admin creates user."}
                )

            from tenants.models import Tenant
            tenant = Tenant.objects.get(id=tenant_id)

    # Tenant Admin Flow
        else:
            tenant = request_user.tenant

        user = User.objects.create_user(
            email=email,
            password=password,
            tenant=tenant,
            **validated_data
        )

    # Assign roles
        for role_name in roles_data:
            role = Role.objects.get(
            tenant=tenant,
            name=role_name
        )
        UserRole.objects.create(user=user, role=role)

        return user
    
    def update(self, instance, validated_data):
        roles_data = validated_data.pop("roles", None)
        password = validated_data.pop("password", None)

        # Update normal fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # Update password securely
        if password:
            instance.set_password(password)

        instance.save()

        # Update roles if provided
        if roles_data is not None:
            instance.user_roles.all().delete()

            tenant = self.context["request"].user.tenant

            for role_name in roles_data:
                role = Role.objects.get(
                    tenant=tenant,
                    name=role_name
                )
                UserRole.objects.create(user=instance, role=role)

        return instance


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ["id", "code", "description"]


class RoleSerializer(serializers.ModelSerializer):
    permissions = serializers.PrimaryKeyRelatedField(
        queryset=Permission.objects.all(),
        many=True,
        write_only=True
    )

    permission_details = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Role
        fields = ["id", "name", "tenant", "permissions", "permission_details"]

    def get_permission_details(self, obj):
        role_permissions = obj.role_permissions.all()
        permissions = [rp.permission for rp in role_permissions]
        return PermissionSerializer(permissions, many=True).data

    def create(self, validated_data):
        permissions = validated_data.pop("permissions", [])
        role = Role.objects.create(**validated_data)

        for permission in permissions:
            RolePermission.objects.create(
                role=role,
                permission=permission
            )

        return role