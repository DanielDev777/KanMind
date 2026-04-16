"""Task and Comment models for the kanban application.

This module defines Task and Comment models which represent individual
tasks on boards and comments on tasks.
"""
from django.db import models

from auth_app.models import CustomUser
from boards.models import Board


class Task(models.Model):
    """Task model representing a work item on a board.

    Tasks belong to a board and can be assigned to users, have
    reviewers, status, priority, and due dates.
    """

    STATUS_CHOICES = [
        ('to-do', 'To Do'),
        ('in-progress', 'In Progress'),
        ('review', 'Review'),
        ('done', 'Done'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]
    
    board = models.ForeignKey(Board, related_name='tasks', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='to-do')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    assignee = models.ForeignKey(CustomUser, null=True, blank=True, related_name='assigned_tasks', on_delete=models.SET_NULL)
    reviewer = models.ForeignKey(CustomUser, null=True, blank=True, related_name='reviewing_tasks', on_delete=models.SET_NULL)
    due_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(CustomUser, related_name='created_tasks', on_delete=models.CASCADE)

    @property
    def comments_count(self):
        """Return the number of comments on this task."""
        return self.comments.count()


class Comment(models.Model):
    """Comment model representing a discussion entry on a task.

    Comments are created by users on specific tasks to provide
    updates, feedback, or discussion points.
    """

    task = models.ForeignKey(Task, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(CustomUser, related_name='comments', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
