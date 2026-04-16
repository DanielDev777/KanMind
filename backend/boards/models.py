"""Board models for the kanban application.

This module defines the Board model which represents a kanban board
with owner, members, and task tracking capabilities.
"""
from django.db import models

from auth_app.models import CustomUser


class Board(models.Model):
    """Kanban board model.

    A board is owned by one user and can have multiple members.
    Tasks are associated with boards, and only board members can
    access and manage tasks on that board.
    """

    title = models.CharField(max_length=255)
    owner = models.ForeignKey(CustomUser, related_name='owned_boards', on_delete=models.CASCADE)
    members = models.ManyToManyField(CustomUser, related_name='boards', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def member_count(self):
        """Return the total number of members including the owner."""
        return self.members.count()
    
    @property
    def ticket_count(self):
        """Return the total number of tasks on this board."""
        return self.tasks.count()
    
    @property
    def tasks_to_do_count(self):
        """Return the number of tasks with 'to-do' status."""
        return self.tasks.filter(status='to-do').count()
    
    @property
    def tasks_high_prio_count(self):
        """Return the number of high priority tasks."""
        return self.tasks.filter(priority='high').count()