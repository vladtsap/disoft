from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from tasks.models import Task, Status, TaskImage, TaskComment
from tasks.permissions import HasEditingPermission, HasCommentingPermission
from tasks.serializers import UserSerializer, TaskSerializer, TaskCommentSerializer


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


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def create_get_tasks(request):
    if request.method == 'GET':
        tasks = Task.objects.all()

        if status_filter := request.GET.get('status'):
            tasks = tasks.filter(status=Status.objects.get(name=status_filter))

        return JsonResponse(TaskSerializer(tasks, many=True).data, safe=False)

    elif request.method == 'POST':
        serializer = TaskSerializer(data=request.data)
        if not serializer.is_valid():
            return JsonResponse(serializer.errors, status=400)

        task = serializer.save(author=request.user)
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


@api_view(['POST'])
@permission_classes([IsAuthenticated, HasEditingPermission])
def upload_images(request, task_id: int):
    task = Task.objects.get(id=task_id)

    for image in request.FILES.getlist('images'):
        task.images.create(image=image)

    return JsonResponse({'message': 'images uploaded'}, status=200)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated, HasCommentingPermission])
def create_get_comments(request, task_id: int):
    task = Task.objects.get(id=task_id)

    if request.method == 'GET':
        return JsonResponse(TaskCommentSerializer(task.comments, many=True).data, safe=False)

    elif request.method == 'POST':
        serializer = TaskCommentSerializer(data=request.data)
        if not serializer.is_valid():
            return JsonResponse(serializer.errors, status=400)
        comment = serializer.save(author=request.user, task=task)
        return JsonResponse({'id': comment.id}, status=201)
