"""Serializers for Board model.

This module provides serializers for different board operations:
list, detail, create, and update operations.
"""
from rest_framework import serializers
from auth_app.models import CustomUser
from boards.models import Board
from auth_app.api.serializers import UserDetailSerializer
from tasks.api.serializers import TaskSerializer


class BoardListSerializer(serializers.ModelSerializer):
    """Serializer for board list view.

    Returns board data with computed counts for members, tickets,
    to-do tasks, and high priority tasks.
    """

    member_count = serializers.ReadOnlyField()
    ticket_count = serializers.ReadOnlyField()
    tasks_to_do_count = serializers.ReadOnlyField()
    tasks_high_prio_count = serializers.ReadOnlyField()
    
    class Meta:
        model = Board
        fields = ['id', 'title', 'owner_id', 'member_count', 'ticket_count', 'tasks_to_do_count', 'tasks_high_prio_count']



class BoardDetailSerializer(serializers.ModelSerializer):
    """Serializer for detailed board view.

    Returns board with nested member details and all associated tasks.
    Used for GET requests on individual board endpoints.
    """

    members = UserDetailSerializer(many=True, read_only=True)
    tasks = TaskSerializer(many=True, read_only=True)
    
    class Meta:
        model = Board
        fields = ['id', 'title', 'owner_id', 'members', 'tasks']


class BoardCreateSerializer(serializers.ModelSerializer):
    """Serializer for board creation.

    Accepts member IDs as input, auto-assigns owner from request user.
    Returns board list format with computed counts.
    """

    members = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all(),
        many=True,
        required=False,
        write_only=True
    )
    
    member_count = serializers.ReadOnlyField()
    ticket_count = serializers.ReadOnlyField()
    tasks_to_do_count = serializers.ReadOnlyField()
    tasks_high_prio_count = serializers.ReadOnlyField()
    owner_id = serializers.ReadOnlyField(source='owner.id')
    
    class Meta:
        model = Board
        fields = ['id', 'title', 'members', 'owner_id', 'member_count', 
                  'ticket_count', 'tasks_to_do_count', 'tasks_high_prio_count']
    
    def create(self, validated_data):
        """Create a new board with the current user as owner.

        Members are set from the provided member IDs.
        """
        members_data = validated_data.pop('members', [])
        request = self.context.get('request')
        current_user = request.user
        
        board = Board.objects.create(
            owner=current_user,
            **validated_data
        )
        
        if members_data:
            board.members.set(members_data)
        
        return board



class BoardUpdateSerializer(serializers.ModelSerializer):
    """Serializer for board updates.

    Accepts member IDs for update, returns detailed owner and member data.
    """

    members = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all(),
        many=True,
        required=False,
        write_only=True
    )
    
    owner_data = serializers.SerializerMethodField()
    members_data = serializers.SerializerMethodField()
    
    class Meta:
        model = Board
        fields = ['id', 'title', 'members', 'owner_data', 'members_data']
    
    def get_owner_data(self, obj):
        """Return detailed owner information."""
        return UserDetailSerializer(obj.owner).data
    
    def get_members_data(self, obj):
        """Return detailed information for all board members."""
        return UserDetailSerializer(obj.members.all(), many=True).data