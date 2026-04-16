from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.db.models import Q
from tasks.models import Task, Comment
from .serializers import TaskSerializer, TaskCreateUpdateSerializer, CommentSerializer, CommentCreateSerializer
from .permissions import IsTaskBoardMember, IsTaskCreatorOrBoardOwner, IsCommentAuthor


class AssignedTasksView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer

    def get_queryset(self):
        return Task.objects.filter(assignee=self.request.user)


class ReviewingTasksView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer

    def get_queryset(self):
        return Task.objects.filter(reviewer=self.request.user)


class TaskListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TaskCreateUpdateSerializer

    def get_queryset(self):
        return Task.objects.filter(
            Q(board__owner=self.request.user) | Q(
                board__members=self.request.user)
        ).distinct()


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsTaskBoardMember]
    queryset = Task.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'PATCH':
            return TaskCreateUpdateSerializer
        return TaskSerializer

    def get_permissions(self):
        if self.request.method == 'DELETE':
            return [IsAuthenticated(), IsTaskCreatorOrBoardOwner()]
        return [IsAuthenticated(), IsTaskBoardMember()]
    

class CommentListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CommentCreateSerializer
        return CommentSerializer

    def get_task_and_check_permission(self):
        """Get the task and verify user is a board member"""
        task = get_object_or_404(Task, pk=self.kwargs['task_id'])
        board = task.board
        
        # Check if user is board owner or member
        if board.owner != self.request.user and self.request.user not in board.members.all():
            raise PermissionDenied("You must be a member of the task's board to access comments.")
        
        return task

    def get_queryset(self):
        task = self.get_task_and_check_permission()
        return Comment.objects.filter(task=task)
    
    def perform_create(self, serializer):
        task = self.get_task_and_check_permission()
        # Pass task in context so CommentCreateSerializer can auto-assign it
        serializer.save(task=task, author=self.request.user)


class CommentDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated, IsCommentAuthor]
    queryset = Comment.objects.all()