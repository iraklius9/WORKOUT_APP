from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django_otp import devices_for_user
from django_otp.plugins.otp_totp.models import TOTPDevice
from django import forms
import qrcode
import qrcode.image.svg
from io import BytesIO
import base64

class EnableTwoFactorForm(forms.Form):
    code = forms.CharField(max_length=6, min_length=6)

def get_user_totp_device(user, confirmed=None):
    devices = devices_for_user(user, confirmed=confirmed)
    for device in devices:
        if isinstance(device, TOTPDevice):
            return device

@login_required
def two_factor_setup(request):
    if request.method == 'GET':
        device = get_user_totp_device(request.user)
        if not device:
            device = TOTPDevice.objects.create(user=request.user, confirmed=False)

        url = device.config_url
        img = qrcode.make(url, image_factory=qrcode.image.svg.SvgImage)
        buffer = BytesIO()
        img.save(buffer)
        qr_code = base64.b64encode(buffer.getvalue()).decode()

        return render(request, 'security/two_factor_setup.html', {
            'qr_code': qr_code,
            'secret_key': device.key,
        })

    if request.method == 'POST':
        code = request.POST.get('code')
        device = get_user_totp_device(request.user)
        
        if device is None:
            return redirect('two_factor_setup')

        if device.verify_token(code):
            device.confirmed = True
            device.save()
            return redirect('two_factor_success')
        
        return render(request, 'security/two_factor_setup.html', {
            'error': 'Invalid code. Please try again.'
        })

@login_required
def two_factor_success(request):
    return render(request, 'security/two_factor_success.html')
