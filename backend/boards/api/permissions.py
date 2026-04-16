"""Permission classes for board operations.

Defines custom permissions for board access control.
"""
from rest_framework.permissions import BasePermission


class IsBoardMember(BasePermission):
    """Allow access only to board owners or members."""

    def has_object_permission(self, request, view, obj):
        """Check if user is the board owner or a member."""
        return obj.owner == request.user or request.user in obj.members.all()


class IsBoardOwner(BasePermission):
    """Allow access only to board owners."""

    def has_object_permission(self, request, view, obj):
        """Check if user is the board owner."""
        return obj.owner == request.user
