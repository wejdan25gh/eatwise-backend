from django.urls import path
from .views import send_otp, verify_otp, my_profile, update_my_profile

urlpatterns = [
    path("send-otp/", send_otp),
    path("verify-otp/", verify_otp),
    path("me/", my_profile),
    path("me/update/", update_my_profile),
]