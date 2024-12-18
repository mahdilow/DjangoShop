from django.urls import path, include
from .views import PhoneLoginView, VerifyOTPView, check_phone
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('phone-login/', PhoneLoginView.as_view(), name='phone_login'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify_otp'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('check-phone/', check_phone, name='check_phone'),
]
