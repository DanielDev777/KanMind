from rest_framework import serializers
from auth_app.models import CustomUser
from boards.models import Board
from auth_app.api.serializers import UserDetailSerializer
from tasks.api.serializers import TaskSerializer


class BoardListSerializer(serializers.ModelSerializer):
    member_count = serializers.ReadOnlyField()
    ticket_count = serializers.ReadOnlyField()
    tasks_to_do_count = serializers.ReadOnlyField()
    tasks_high_prio_count = serializers.ReadOnlyField()
    
    class Meta:
        model = Board
        fields = ['id', 'title', 'owner_id', 'member_count', 'ticket_count', 'tasks_to_do_count', 'tasks_high_prio_count']


class BoardDetailSerializer(serializers.ModelSerializer):
    members = UserDetailSerializer(many=True, read_only=True)
    tasks = TaskSerializer(many=True, read_only=True)
    
    class Meta:
        model = Board
        fields = ['id', 'title', 'owner_id', 'members', 'tasks']

class BoardCreateSerializer(serializers.ModelSerializer):
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
        return UserDetailSerializer(obj.owner).data
    
    def get_members_data(self, obj):
        return UserDetailSerializer(obj.members.all(), many=True).data