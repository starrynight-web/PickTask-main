from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.utils import timezone
import uuid

from .forms import UserRegisterForm, UserLoginForm, CustomPasswordResetForm, CustomSetPasswordForm
from .models import EmailVerification, PasswordResetToken
from .utils import send_verification_email, send_password_reset_email

User = get_user_model()

def register_view(request):
    if request.user.is_authenticated:
        return redirect('workspace:home')
        
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            try:
                user = form.save(commit=False)
                # TEMPORARY FIX: Activate user immediately without email verification
                user.is_active = True  # Changed from False to True
                user.save()
             
                # TEMPORARY FIX: Comment out email verification
                # verification = EmailVerification.objects.create(user=user)
                # send_verification_email(request, user, verification.token)
                
                messages.success(
                    request, 
                    'Account created successfully! You can now log in.'  # Updated message
                )
                return redirect('authentication:login')  # Redirect to login instead
            except Exception as e:
                print(f"Registration error: {e}")
                messages.error(
                    request,
                    'An error occurred during registration. Please try again.'
                )
    else:
        form = UserRegisterForm()
    
    return render(request, 'authentication/register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('workspace:home')
        
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
          
            # TEMPORARY FIX: Remove email verification check
            # try:
            #     verification = EmailVerification.objects.get(user=user)
            #     if not verification.is_verified:
            #         messages.error(
            #             request, 
            #             'Please verify your email before logging in. '
            #             'Check your email for the verification link.'
            #         )
            #         return redirect('authentication:login')
            # except EmailVerification.DoesNotExist:
            #     pass
                
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            
            next_url = request.GET.get('next', 'workspace:home')
            return redirect(next_url)
    else:
        form = UserLoginForm()
    
    return render(request, 'authentication/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('authentication:login')

def email_verification_sent_view(request):
    return render(request, 'authentication/email_verification_sent.html')

def verify_email_view(request, token):
    try:
        verification = EmailVerification.objects.get(token=token)
        
        if verification.is_verified:
            messages.info(request, 'Email is already verified.')
        else:
            verification.is_verified = True
            verification.save()
        
            user = verification.user
            user.is_active = True
            user.save()
            
            messages.success(request, 'Email verified successfully! You can now log in.')
            return redirect('authentication:email_verification_success')
            
    except EmailVerification.DoesNotExist:
        return render(request, 'authentication/email_verification_failed.html')
    
    return redirect('authentication:login')

def email_verification_success_view(request):
    return render(request, 'authentication/email_verification_success.html')

def password_reset_view(request):
    if request.method == 'POST':
        form = CustomPasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            associated_users = User.objects.filter(email=email)
            
            if associated_users.exists():
                for user in associated_users:
                    # TEMPORARY FIX: Comment out password reset email
                    # reset_token = PasswordResetToken.objects.create(user=user)
                    # send_password_reset_email(request, user, reset_token.token)
                    pass
            
            messages.success(
                request,
                'Password reset feature is temporarily disabled. Please contact support.'
            )
            return redirect('authentication:password_reset_done')
    else:
        form = CustomPasswordResetForm()
    
    return render(request, 'authentication/password_reset.html', {'form': form})

def password_reset_confirm_view(request, token):
    try:
        reset_token = PasswordResetToken.objects.get(token=token)
        
        if reset_token.is_used or reset_token.is_expired():
            messages.error(request, 'This reset link is invalid or has expired.')
            return redirect('authentication:password_reset')
        
        if request.method == 'POST':
            form = CustomSetPasswordForm(reset_token.user, request.POST)
            if form.is_valid():
                form.save()
                reset_token.is_used = True
                reset_token.save()
                
                messages.success(request, 'Password reset successfully! You can now log in.')
                return redirect('authentication:password_reset_complete')
        else:
            form = CustomSetPasswordForm(reset_token.user)
        
        return render(request, 'authentication/password_reset_confirm.html', {'form': form})
        
    except PasswordResetToken.DoesNotExist:
        messages.error(request, 'Invalid reset token.')
        return redirect('authentication:password_reset')

def password_reset_done_view(request):
    return render(request, 'authentication/password_reset_done.html')

def password_reset_complete_view(request):
    return render(request, 'authentication/password_reset_complete.html')

@login_required
def resend_verification_email_view(request):
    # TEMPORARY FIX: Disable resend verification
    messages.info(request, 'Email verification is temporarily disabled. Your account is already active.')
    return redirect('workspace:home')