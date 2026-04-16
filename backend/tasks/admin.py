"""Django admin configuration for Task and Comment models."""
from django.contrib import admin
from .models import Task, Comment


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """Admin interface for Task model.

    Displays task details including board, status, priority, and assignment.
    """

    list_display = ['title', 'board', 'status', 'priority', 'assignee', 'created_by']
    list_filter = ['status', 'priority', 'created_at']
    search_fields = ['title', 'description', 'board__title']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Admin interface for Comment model.

    Displays comment preview, author, task, and creation date.
    """

    list_display = ['get_content_preview', 'author', 'task', 'created_at']
    list_filter = ['created_at']
    search_fields = ['content', 'author__fullname', 'task__title']
    
    def get_content_preview(self, obj):
        """Return a truncated preview of the comment content."""
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    get_content_preview.short_description = 'Content'
