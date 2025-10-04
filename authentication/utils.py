from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

def send_verification_email(request, user, token):
    subject = 'Verify Your Email - PickTask'
    
    verification_url = f"{settings.SITE_URL}/auth/verify-email/{token}/"
    
    html_message = render_to_string('authentication/activation_email.html', {
        'user': user,
        'verification_url': verification_url,
    })
    
    plain_message = strip_tags(html_message)
    
    send_mail(
        subject,
        plain_message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        html_message=html_message,
        fail_silently=False,
    )

def send_password_reset_email(request, user, token):
    subject = 'Reset Your Password - PickTask'
    
    reset_url = f"{settings.SITE_URL}/auth/password-reset-confirm/{token}/"
    
    html_message = render_to_string('authentication/password_reset_email.html', {
        'user': user,
        'reset_url': reset_url,
    })
    
    plain_message = strip_tags(html_message)
    
    send_mail(
        subject,
        plain_message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        html_message=html_message,
        fail_silently=False,
    )