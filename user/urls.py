from django.urls import path

from .views import (
    UserRegistrationView, 
    UserLoginView, 
    VerifyOTPView, 
    PasswordResetRequestView, 
    ResetPasswordVerifyOTPView, 
    PasswordResetView,
    ForgotPasswordRequestView,
    ForgotPasswordVerifyOTPView,
    ForgotPasswordResetView,
    UserDevicesView,
    RemoveDeviceView,
)

urlpatterns = [

    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('register-verify-otp/', VerifyOTPView.as_view(), name='register-verify-otp'),

    path('devices/', UserDevicesView.as_view(), name='devices'),
    path('remove-device/', RemoveDeviceView.as_view(), name='remove-device'),

    path('reset-password/', PasswordResetRequestView.as_view(), name='reset-password'),
    path('reset-password-verify-otp/', ResetPasswordVerifyOTPView.as_view(), name='reset-password-verify-otp'),
    path('confirm-reset-password/', PasswordResetView.as_view(), name='confirm-password'),

    path('forgot-password/', ForgotPasswordRequestView.as_view(), name='reset-password'),
    path('forgot-password-verify-otp/', ForgotPasswordVerifyOTPView.as_view(), name='reset-password-verify-otp'),
    path('confirm-forgot-password/', ForgotPasswordResetView.as_view(), name='confirm-forgot-password'),

]