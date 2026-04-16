"""API views for board operations.

Provides endpoints for listing, creating, retrieving, updating,
and deleting boards with proper permission controls.
"""
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from boards.models import Board
from .serializers import BoardCreateSerializer, BoardListSerializer, BoardDetailSerializer, BoardUpdateSerializer
from .permissions import IsBoardMember, IsBoardOwner


class BoardListCreateView(generics.ListCreateAPIView):
    """List boards and create new boards.

    GET: Return boards where user is owner or member.
    POST: Create a new board with the current user as owner.
    """

    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Return boards where user is owner or member."""
        return Board.objects.filter(
            Q(owner=self.request.user) | Q(members=self.request.user)
        ).distinct()
    
    def get_serializer_class(self):
        """Return appropriate serializer based on request method."""
        if self.request.method == 'POST':
            return BoardCreateSerializer
        return BoardListSerializer


class BoardDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a board.

    GET/PATCH: Available to board members.
    DELETE: Only available to board owner.
    """

    queryset = Board.objects.all()
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        """Return appropriate serializer based on request method."""
        if self.request.method == 'PATCH':
            return BoardUpdateSerializer
        return BoardDetailSerializer
    
    def get_permissions(self):
        """Return appropriate permissions based on request method."""
        if self.request.method == 'DELETE':
            return [IsAuthenticated(), IsBoardOwner()]
        return [IsAuthenticated(), IsBoardMember()]