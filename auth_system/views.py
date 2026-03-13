import random
from datetime import timedelta

from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User

from .models import OTP
from .serializers import SendOTPSerializer, VerifyOTPSerializer


def generate_otp(length: int = 6) -> str:
    return str(random.randint(10 ** (length - 1), 10 ** length - 1))


class SendOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SendOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.get("email")
        phone = serializer.validated_data.get("phone")

        print("API HIT: SendOTP")

        otp = generate_otp()

        OTP.objects.create(
            email=email or "",
            phone=phone or "",
            otp_code=otp,
            expires_at=timezone.now() + timedelta(minutes=5),
        )

        print(f"OTP: {otp}")

        return Response(
            {"message": "OTP sent successfully", "otp_length": 6},
            status=status.HTTP_200_OK,
        )


class VerifyOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.get("email")
        phone = serializer.validated_data.get("phone")
        otp_code = serializer.validated_data["otp"]

        print(f"API HIT: VerifyOTP for {email or phone}")

        otp_obj = OTP.objects.filter(
            email=email or "",
            phone=phone or "",
            otp_code=otp_code,
            is_used=False,
            expires_at__gte=timezone.now(),
        ).last()

        if not otp_obj:
            return Response(
                {"error": "Invalid or expired OTP"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        otp_obj.mark_used()

        # Get or create user
        user, created = User.objects.get_or_create(
            email=email if email else f"phone_{phone}@auto.local",
            defaults={
                "phone": phone,
                "is_active": True,
            },
        )

        if created:
            print(f"New user created: {user.email}")

        # Issue JWT token
        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "user_id": user.id,
                "email": user.email,
                "is_new_user": created,
            },
            status=status.HTTP_200_OK,
        )

