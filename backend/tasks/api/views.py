from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from boards.models import Board
from tasks.models import Task
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
    queryset = Task.objects.all()
    permission_classes = [IsTaskBoardMember]

    def get_serializer_class(self):
        if self.request.method == 'PATCH':
            return TaskCreateUpdateSerializer
        return TaskSerializer

    def get_permissions(self):
        if self.request.method == 'DELETE':
            return [IsAuthenticated(), IsTaskCreatorOrBoardOwner()]
        return [IsAuthenticated(), IsTaskBoardMember()]
