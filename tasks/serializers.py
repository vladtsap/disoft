from django.contrib.auth.models import User
from rest_framework import serializers

from tasks.models import Task, TaskAssignee, Status


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
    status = serializers.CharField(required=False)
    assignee = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all(), required=False)

    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ('author',)

    def create(self, validated_data):
        assignee = validated_data.pop('assignee', [])
        status_data = validated_data.pop('status', None)

        task = Task.objects.create(**validated_data)

        for user in assignee:
            TaskAssignee.objects.create(user=user, task=task)

        if status_data:
            status = Status.objects.get(name=status_data)
            task.status = status
            task.save()

        return task

    def update(self, instance, validated_data):
        status_data = validated_data.pop('status', None)
        instance = super().update(instance, validated_data)

        if status_data:
            status = Status.objects.get(name=status_data)
            instance.status = status
            instance.save()

        return instance
