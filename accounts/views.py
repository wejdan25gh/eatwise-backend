import random
from datetime import timedelta

from django.utils import timezone
from django.contrib.auth.models import User

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from .models import OTPCode, UserProfile


@api_view(["POST"])
def send_otp(request):
    phone_number = request.data.get("phone_number")

    if not phone_number:
        return Response(
            {"error": "phone_number is required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    code = f"{random.randint(0, 999999):06d}"
    expires_at = timezone.now() + timedelta(minutes=3)

    OTPCode.objects.create(
        phone_number=phone_number,
        code=code,
        expires_at=expires_at
    )

    print(f"[DEV OTP] Phone: {phone_number}  Code: {code}  Expires: {expires_at}")

    return Response(
        {"message": "OTP generated (check server console in development)."},
        status=status.HTTP_200_OK
    )


@api_view(["POST"])
def verify_otp(request):
    phone_number = request.data.get("phone_number")
    code = request.data.get("code")

    if not phone_number or not code:
        return Response(
            {"error": "phone_number and code are required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    otp = OTPCode.objects.filter(phone_number=phone_number).order_by("-created_at").first()

    if not otp:
        return Response({"error": "No OTP found"}, status=status.HTTP_400_BAD_REQUEST)

    if timezone.now() > otp.expires_at:
        return Response({"error": "OTP expired"}, status=status.HTTP_400_BAD_REQUEST)

    if otp.code != str(code):
        return Response({"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)

    username = f"user_{phone_number}"
    user, _ = User.objects.get_or_create(username=username)

    profile = UserProfile.objects.filter(phone_number=phone_number).first()
    if profile:
        if profile.user_id != user.id:
            profile.user = user
            profile.save()
    else:
        UserProfile.objects.create(user=user, phone_number=phone_number)

    refresh = RefreshToken.for_user(user)

    return Response(
        {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        },
        status=status.HTTP_200_OK
    )



@api_view(["GET"])
@permission_classes([IsAuthenticated])
def my_profile(request):
    profile = UserProfile.objects.filter(user=request.user).first()

    if not profile:
        return Response({"error": "Profile not found"}, status=404)

    return Response({
        "id": profile.id,
        "phone_number": profile.phone_number,
        "full_name": profile.full_name,
        "age": profile.age,
        "allergies": profile.allergies,
    })

    
@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def update_my_profile(request):
    """
    Update current user's profile fields.
    Allowed fields: full_name, age, allergies
    """
    profile = UserProfile.objects.filter(user=request.user).first()
    if not profile:
        return Response({"error": "Profile not found"}, status=404)

    full_name = request.data.get("full_name")
    age = request.data.get("age")
    allergies = request.data.get("allergies")

    if full_name is not None:
        profile.full_name = full_name

    if age is not None:
        try:
            profile.age = int(age)
        except ValueError:
            return Response({"error": "age must be a number"}, status=400)

    if allergies is not None:
        profile.allergies = allergies

    profile.save()

    return Response({
        "message": "Profile updated",
        "profile": {
            "id": profile.id,
            "phone_number": profile.phone_number,
            "full_name": profile.full_name,
            "age": profile.age,
            "allergies": profile.allergies,
        }
    })