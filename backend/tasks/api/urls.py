"""URL routing for task and comment API endpoints."""
from django.urls import path
from .views import TaskListCreateView, TaskDetailView, AssignedTasksView, ReviewingTasksView, CommentListCreateView, CommentDeleteView


urlpatterns = [
    path('tasks/', TaskListCreateView.as_view()),
    path('tasks/assigned-to-me/', AssignedTasksView.as_view()),
    path('tasks/reviewing/', ReviewingTasksView.as_view()),
    path('tasks/<int:pk>/', TaskDetailView.as_view()),
    path('tasks/<int:task_id>/comments/', CommentListCreateView.as_view()),
    path('tasks/<int:task_id>/comments/<int:pk>/', CommentDeleteView.as_view()),
]