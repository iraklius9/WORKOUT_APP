from django.urls import path
from . import two_factor

urlpatterns = [
    # 2FA URLs
    path('2fa/setup/', two_factor.two_factor_setup, name='two_factor_setup'),
    path('2fa/success/', two_factor.two_factor_success, name='two_factor_success'),
]
