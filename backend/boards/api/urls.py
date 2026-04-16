"""URL routing for board API endpoints."""
from django.urls import path
from .views import BoardListCreateView, BoardDetailView

urlpatterns = [
    path('boards/', BoardListCreateView.as_view()),
    path('boards/<int:pk>/', BoardDetailView.as_view()),
]