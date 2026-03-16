from rest_framework import serializers


class SendOTPSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)
    phone = serializers.CharField(max_length=20, required=False)

    def validate(self, data):
        if not data.get('email') and not data.get('phone'):
            raise serializers.ValidationError(
                "Either email or phone must be provided."
            )
        return data


class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)
    phone = serializers.CharField(max_length=20, required=False)
    otp = serializers.CharField(max_length=6, min_length=4)

    def validate(self, data):
        if not data.get('email') and not data.get('phone'):
            raise serializers.ValidationError(
                "Either email or phone must be provided."
            )
        return data
