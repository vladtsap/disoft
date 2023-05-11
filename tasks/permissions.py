from rest_framework.permissions import BasePermission

from tasks.models import Task, Status, TaskAssignee


class HasEditingPermission(BasePermission):
    def has_permission(self, request, view):
        if 'task_id' not in view.kwargs:
            return False

        task = Task.objects.get(id=view.kwargs['task_id'])

        if task.author == request.user:
            # author always has permission to edit
            return True

        elif request.method == 'PUT' and request.data.keys() == {'status'}:
            # assignee can only change status of task (except for New and Done)
            return TaskAssignee.objects.filter(user=request.user, task=task).exists() and \
                Status.objects.filter(name=request.data['status']).exclude(name__in=['New', 'Done']).exists()

        else:
            return False


class HasCommentingPermission(BasePermission):
    def has_permission(self, request, view):
        if 'task_id' not in view.kwargs:
            return False

        task = Task.objects.get(id=view.kwargs['task_id'])

        return task.author == request.user or \
            TaskAssignee.objects.filter(user=request.user, task=task).exists() or \
            request.user.is_admin
