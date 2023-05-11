from rest_framework.permissions import BasePermission

from tasks.models import Task


class IsTaskAuthor(BasePermission):
    def has_permission(self, request, view):
        if 'task_id' not in view.kwargs:
            return False

        task = Task.objects.get(id=view.kwargs['task_id'])

        return task.author == request.user
