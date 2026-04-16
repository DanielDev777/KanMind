"""API views for task and comment operations.

Provides endpoints for task management, filtering, and commenting
with board membership validation and permission controls.
"""
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.db.models import Q
from tasks.models import Task, Comment
from .serializers import TaskSerializer, TaskCreateUpdateSerializer, CommentSerializer, CommentCreateSerializer
from .permissions import IsTaskBoardMember, IsTaskCreatorOrBoardOwner, IsCommentAuthor


class AssignedTasksView(generics.ListAPIView):
    """List tasks assigned to the current user.

    Return all tasks where the user is the assignee.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer

    def get_queryset(self):
        """Return tasks assigned to the current user."""
        return Task.objects.filter(assignee=self.request.user)


class ReviewingTasksView(generics.ListAPIView):
    """List tasks being reviewed by the current user.

    Return all tasks where the user is the reviewer.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer

    def get_queryset(self):
        """Return tasks where the current user is the reviewer."""
        return Task.objects.filter(reviewer=self.request.user)


class TaskListCreateView(generics.ListCreateAPIView):
    """List tasks and create new tasks.

    GET: Return tasks from boards where user is owner or member.
    POST: Create a new task on a board (validates board membership).
    """

    permission_classes = [IsAuthenticated]
    serializer_class = TaskCreateUpdateSerializer

    def get_queryset(self):
        """Return tasks from boards where user is owner or member."""
        return Task.objects.filter(
            Q(board__owner=self.request.user) | Q(
                board__members=self.request.user)
        ).distinct()


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a task.

    GET/PATCH: Available to board members.
    DELETE: Only available to task creator or board owner.
    """

    permission_classes = [IsTaskBoardMember]
    queryset = Task.objects.all()

    def get_serializer_class(self):
        """Return appropriate serializer based on request method."""
        if self.request.method == 'PATCH':
            return TaskCreateUpdateSerializer
        return TaskSerializer

    def get_permissions(self):
        """Return appropriate permissions based on request method."""
        if self.request.method == 'DELETE':
            return [IsAuthenticated(), IsTaskCreatorOrBoardOwner()]
        return [IsAuthenticated(), IsTaskBoardMember()]
    


class CommentListCreateView(generics.ListCreateAPIView):
    """List and create comments on a task.

    Validate that user is a member of the task's board before
    allowing access to comments.
    """

    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        """Return appropriate serializer based on request method."""
        if self.request.method == 'POST':
            return CommentCreateSerializer
        return CommentSerializer

    def get_task_and_check_permission(self):
        """Get the task and verify user is a board member.

        Raises PermissionDenied if user is not a member of the task's board.
        """
        task = get_object_or_404(Task, pk=self.kwargs['task_id'])
        board = task.board
        
        # Check if user is board owner or member
        if board.owner != self.request.user and self.request.user not in board.members.all():
            raise PermissionDenied("You must be a member of the task's board to access comments.")
        
        return task

    def get_queryset(self):
        """Return comments for the task if user has access."""
        task = self.get_task_and_check_permission()
        return Comment.objects.filter(task=task)
    
    def perform_create(self, serializer):
        """Create comment with auto-assigned task and author."""
        task = self.get_task_and_check_permission()
        # Pass task in context so CommentCreateSerializer can auto-assign it
        serializer.save(task=task, author=self.request.user)


class CommentDeleteView(generics.DestroyAPIView):
    """Delete a comment.

    Only the comment author can delete their own comments.
    """

    permission_classes = [IsAuthenticated, IsCommentAuthor]
    queryset = Comment.objects.all()