from rest_framework import serializers
from .models import TenantSetting, Tenant
from .constants import TENANT_SETTING_CHOICES


class TenantSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tenant
        fields = [
            'id',
            'name',
            'domain',
            'slug',
            'contact_email',
            'is_active',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_domain(self, value):
        return value.lower()


class TenantSettingSerializer(serializers.ModelSerializer):

    class Meta:
        model = TenantSetting
        fields = ['id', 'key', 'value', 'created_at']
        read_only_fields = ['id', 'created_at']
    
    

    def validate_key(self, value):
        valid_keys = [choice[0] for choice in TENANT_SETTING_CHOICES]
        if value not in valid_keys:
            raise serializers.ValidationError(
                f"Invalid key. Valid keys are: {valid_keys}"
            )
        return value

    def validate(self, attrs):
        """
        Prevent tenant key duplication manually
        (gives cleaner error than DB IntegrityError)
        """
        request = self.context.get("request")
        tenant = request.user.tenant

        if TenantSetting.objects.filter(
            tenant=tenant,
            key=attrs["key"]
        ).exists():
            raise serializers.ValidationError(
                {"key": "This setting already exists for this tenant."}
            )

        return attrs
    
    def create(self, validated_data):
        request = self.context.get("request")
        return TenantSetting.objects.create(
            tenant=request.user.tenant,
            **validated_data
    )