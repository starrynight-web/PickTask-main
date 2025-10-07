from django.urls import path
from . import views

app_name = 'authentication'

urlpatterns = [
    # Registration & Login
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'), 
    # Email Verification
    path('verify-email/sent/', views.email_verification_sent_view, name='email_verification_sent'),
    path('verify-email/<uuid:token>/', views.verify_email_view, name='verify_email'),
    path('verify-email/success/', views.email_verification_success_view, name='email_verification_success'),
    path('resend-verification/', views.resend_verification_email_view, name='resend_verification'),   
    # Password Reset
    path('password-reset/', views.password_reset_view, name='password_reset'),
    path('password-reset/done/', views.password_reset_done_view, name='password_reset_done'),
    path('password-reset-confirm/<uuid:token>/', views.password_reset_confirm_view, name='password_reset_confirm'),
    path('password-reset/complete/', views.password_reset_complete_view, name='password_reset_complete'),
]