"""Django admin configuration for Board model."""
from django.contrib import admin
from .models import Board


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    """Admin interface for Board model.

    Displays id, title, owner, member count, member names, and creation date.
    """

    list_display = ['id', 'title', 'owner', 'get_member_count', 'get_members', 'created_at']
    search_fields = ['title', 'owner__fullname', 'owner__email']
    list_filter = ['created_at']
    filter_horizontal = ['members']
    
    def get_member_count(self, obj):
        """Return the member count for display."""
        return obj.member_count
    get_member_count.short_description = 'Member Count'
    
    def get_members(self, obj):
        """Return comma-separated list of member names."""
        return ", ".join([member.fullname for member in obj.members.all()])
    get_members.short_description = 'Members'
