from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from tasks.models import Task, Status
from tasks.permissions import HasEditingPermission
from tasks.serializers import UserSerializer, TaskSerializer


@api_view(['GET'])
def hello_world(request):
    return JsonResponse({'message': 'Hello, world!'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def hello(request):
    user = request.user
    return JsonResponse({'message': f'Hello, {user.username}!'})


@api_view(['POST'])
def sign_up(request):
    serializer = UserSerializer(data=request.data)
    if not serializer.is_valid():
        return JsonResponse(serializer.errors, status=400)

    user = serializer.save()
    return JsonResponse({'username': user.username}, status=201)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_task(request):
    user = request.user

    serializer = TaskSerializer(data=request.data)
    if not serializer.is_valid():
        return JsonResponse(serializer.errors, status=400)

    task = serializer.save(author=user)
    return JsonResponse({'id': task.id}, status=201)


@api_view(['PUT', 'DELETE'])
@permission_classes([IsAuthenticated, HasEditingPermission])
def edit_delete_task(request, task_id: int):
    task = Task.objects.get(id=task_id)

    if request.method == 'PUT':
        serializer = TaskSerializer(instance=task, data=request.data, partial=True)
        if not serializer.is_valid():
            return JsonResponse(serializer.errors, status=400)

        task = serializer.save()
        return JsonResponse({'id': task.id}, status=200)

    elif request.method == 'DELETE':
        task.delete()
        return JsonResponse({'message': 'task deleted'}, status=200)
