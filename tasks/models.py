from django.contrib.auth.models import User
from django.db import models


class Status(models.Model):
    name = models.CharField(max_length=200)


class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    assignee = models.ManyToManyField(User, through='TaskAssignee', related_name='assigned_tasks', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class TaskAssignee(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'task')
