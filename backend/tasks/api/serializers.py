from rest_framework import serializers
from auth_app.api.serializers import UserDetailSerializer
from auth_app.models import CustomUser
from tasks.models import Task, Comment


class TaskSerializer(serializers.ModelSerializer):
    assignee = UserDetailSerializer(read_only=True)
    reviewer = UserDetailSerializer(read_only=True)
    comments_count = serializers.ReadOnlyField()
    
    class Meta:
        model = Task
        fields = ['id', 'board', 'title', 'description', 'status', 'priority', 
                  'assignee', 'reviewer', 'due_date', 'comments_count']


class TaskCreateUpdateSerializer(serializers.ModelSerializer):
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
        request = self.context.get('request')
        validated_data['created_by'] = request.user
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        if 'board' in validated_data and validated_data['board'] != instance.board:
            raise serializers.ValidationError({
                "board": "Board cannot be changed after task creation."
            })
        return super().update(instance, validated_data)
    
    def to_representation(self, instance):
        return TaskSerializer(instance, context=self.context).data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    
    class Meta:
        model = Comment
        fields = ['id', 'created_at', 'author', 'content']
    
    def get_author(self, obj):
        return obj.author.fullname


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['content']
    
    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['author'] = request.user
        validated_data['task'] = self.context.get('task')
        return super().create(validated_data)
    
    def to_representation(self, instance):
        return CommentSerializer(instance).data
