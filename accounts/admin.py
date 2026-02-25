from django.contrib import admin
from .models import UserProfile, OTPCode

admin.site.register(UserProfile)
admin.site.register(OTPCode)