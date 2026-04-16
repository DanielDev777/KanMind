"""Serializers for Task and Comment models.

Provides serializers for task and comment operations including
create, update, and read operations with proper validation.
"""
from rest_framework import serializers
from auth_app.api.serializers import UserDetailSerializer
from auth_app.models import CustomUser
from tasks.models import Task, Comment


class TaskSerializer(serializers.ModelSerializer):
    """Read-only serializer for task display.

    Returns task data with nested assignee and reviewer details.
    Used for GET requests and as output format for task operations.
    """

    assignee = UserDetailSerializer(read_only=True)
    reviewer = UserDetailSerializer(read_only=True)
    comments_count = serializers.ReadOnlyField()
    
    class Meta:
        model = Task
        fields = ['id', 'board', 'title', 'description', 'status', 'priority', 
                  'assignee', 'reviewer', 'due_date', 'comments_count']


class TaskCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for task creation and updates.

    Accepts assignee_id and reviewer_id as input, validates board membership,
    auto-assigns created_by, and prevents board changes on update.
    """

    assignee_id = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all(),
        source='assignee',
        required=False,
        allow_null=True
    )
    reviewer_id = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all(),
        source='reviewer',
        required=False,
        allow_null=True
    )
    
    class Meta:
        model = Task
        fields = ['board', 'title', 'description', 'status', 'priority', 
                  'assignee_id', 'reviewer_id', 'due_date']
    
    def validate(self, data):
        """Validate that assignee and reviewer are board members.

        Raises ValidationError if assignee or reviewer is not a member
        of the task's board.
        """
        board = data.get('board')
        assignee = data.get('assignee')
        reviewer = data.get('reviewer')
        
        if board:
            board_members = list(board.members.all()) + [board.owner]
            
            if assignee and assignee not in board_members:
                raise serializers.ValidationError({
                    "assignee_id": "Assignee must be a member of the board."
                })
            
            if reviewer and reviewer not in board_members:
                raise serializers.ValidationError({
                    "reviewer_id": "Reviewer must be a member of the board."
                })
        
        return data
    
    def create(self, validated_data):
        """Create a new task with the current user as creator."""
        request = self.context.get('request')
        validated_data['created_by'] = request.user
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        """Update task, preventing board changes.

        Raises ValidationError if attempting to change the board field.
        """
        if 'board' in validated_data and validated_data['board'] != instance.board:
            raise serializers.ValidationError({
                "board": "Board cannot be changed after task creation."
            })
        return super().update(instance, validated_data)
    
    def to_representation(self, instance):
        """Return task in TaskSerializer format for consistent output."""
        return TaskSerializer(instance, context=self.context).data


class CommentSerializer(serializers.ModelSerializer):
    """Read-only serializer for comment display.

    Returns comment with author's full name as a string.
    """

    author = serializers.SerializerMethodField()
    
    class Meta:
        model = Comment
        fields = ['id', 'created_at', 'author', 'content']
    
    def get_author(self, obj):
        """Return the author's full name."""
        return obj.author.fullname


class CommentCreateSerializer(serializers.ModelSerializer):
    """Serializer for comment creation.

    Auto-assigns author from request user and task from context.
    """

    class Meta:
        model = Comment
        fields = ['content']
    
    def create(self, validated_data):
        """Create a new comment with auto-assigned author and task."""
        request = self.context.get('request')
        validated_data['author'] = request.user
        validated_data['task'] = self.context.get('task')
        return super().create(validated_data)
    
    def to_representation(self, instance):
        """Return comment in CommentSerializer format for consistent output."""
        return CommentSerializer(instance).data
