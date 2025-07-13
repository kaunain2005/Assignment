from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Client, Project

# ✅ 1) User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

# ✅ 2) Project Serializer (for output)
class ProjectSerializer(serializers.ModelSerializer):
    users = UserSerializer(many=True, read_only=True)
    client = serializers.StringRelatedField()
    created_by = serializers.StringRelatedField()

    class Meta:
        model = Project
        fields = ['id', 'project_name', 'client', 'users', 'created_at', 'created_by']

# ✅ 3) Project Create Serializer (for POST)
class ProjectCreateSerializer(serializers.ModelSerializer):
    users = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True)

    class Meta:
        model = Project
        fields = ['id', 'project_name', 'users', 'created_at', 'created_by']

    def create(self, validated_data):
        users = validated_data.pop('users')
        project = Project.objects.create(**validated_data)
        project.users.set(users)
        return project

# ✅ 4) Client Serializer (for list/create/update)
class ClientSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Client
        fields = ['id', 'client_name', 'created_at', 'updated_at', 'created_by']

# ✅ 5) Client Detail Serializer (for GET /clients/:id)
class ClientDetailSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField(read_only=True)
    projects = ProjectSerializer(many=True, read_only=True)

    class Meta:
        model = Client
        fields = ['id', 'client_name', 'projects', 'created_at', 'updated_at', 'created_by']
