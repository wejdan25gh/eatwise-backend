from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    # Link each profile to exactly one Django user account
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Phone number for mobile login
    phone_number = models.CharField(max_length=20, unique=True)

    # Basic profile info
    full_name = models.CharField(max_length=150, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    allergies = models.TextField(blank=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.phone_number} ({self.user.username})"




class OTPCode(models.Model):
    # The phone number that requested the OTP
    phone_number = models.CharField(max_length=20)

    # The one-time password code (we store it as text to preserve leading zeros)
    code = models.CharField(max_length=6)

    # Expiration time (after this, the OTP is invalid)
    expires_at = models.DateTimeField()

    # Timestamps for tracking
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"OTP for {self.phone_number} (expires {self.expires_at})"