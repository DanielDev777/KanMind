"""Django admin configuration for Board model."""
from django.contrib import admin
from .models import Board


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    """Admin interface for Board model.

    Displays title, owner, member count, and creation date.
    """

    list_display = ['title', 'owner', 'get_member_count', 'created_at']
    search_fields = ['title', 'owner__fullname', 'owner__email']
    list_filter = ['created_at']
    
    def get_member_count(self, obj):
        """Return the member count for display."""
        return obj.member_count
    get_member_count.short_description = 'Members'
