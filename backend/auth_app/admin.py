"""Django admin configuration for CustomUser model."""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """Admin interface for CustomUser model.

    Extends Django's UserAdmin to include the fullname field.
    """

    list_display = ['email', 'fullname', 'is_staff', 'is_active', 'date_joined']
    search_fields = ['email', 'fullname']
    list_filter = ['is_staff', 'is_active', 'date_joined']
    
    # Add fullname to the fieldsets for editing users
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('fullname',)}),
    )
