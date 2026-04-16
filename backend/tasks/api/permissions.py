"""Permission classes for task and comment operations.

Defines custom permissions for task and comment access control.
"""
from rest_framework.permissions import BasePermission


class IsTaskBoardMember(BasePermission):
    """Allow access only to members of the task's board."""

    def has_object_permission(self, request, view, obj):
        """Check if user is a member of the task's board."""
        board = obj.board
        return board.owner == request.user or request.user in board.members.all()


class IsTaskCreatorOrBoardOwner(BasePermission):
    """Allow access to task creator or board owner."""

    def has_object_permission(self, request, view, obj):
        """Check if user is the task creator or board owner."""
        board = obj.board
        return obj.created_by == request.user or board.owner == request.user


class IsCommentAuthor(BasePermission):
    """Allow access only to the comment author."""

    def has_object_permission(self, request, view, obj):
        """Check if user is the comment author."""
        return obj.author == request.user
