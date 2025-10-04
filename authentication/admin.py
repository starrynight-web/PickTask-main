from django.contrib import admin
from .models import EmailVerification, PasswordResetToken

@admin.register(EmailVerification)
class EmailVerificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'is_verified', 'created_at']
    list_filter = ['is_verified', 'created_at']
    search_fields = ['user__username', 'user__email']

@admin.register(PasswordResetToken)
class PasswordResetTokenAdmin(admin.ModelAdmin):
    list_display = ['user', 'is_used', 'created_at']
    list_filter = ['is_used', 'created_at']
    readonly_fields = ['token', 'created_at']
