from django.contrib.auth.models import User
from rest_framework import serializers

from tasks.models import Task, TaskAssignee


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
        )
        return user

    class Meta:
        model = User
        fields = ('username', 'password')


class TaskSerializer(serializers.ModelSerializer):
    assignee = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all(), required=False)

    def create(self, validated_data):
        assignee = validated_data.pop('assignee', [])
        task = Task.objects.create(**validated_data)
        for user in assignee:
            TaskAssignee.objects.create(user=user, task=task)
        return task

    class Meta:
        model = Task
        fields = ('title', 'description', 'assignee')
