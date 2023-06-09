from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from tasks import views

urlpatterns = [
    path('hello-world', views.hello_world),
    path('hello', views.hello),
    path('sign-up', views.sign_up),
    path('token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('tasks', views.create_get_tasks),
    path('tasks/<int:task_id>', views.edit_delete_task),
    path('tasks/<int:task_id>/images', views.upload_images),
    path('tasks/<int:task_id>/comments', views.create_get_comments),
    path('tasks/<int:task_id>/comments/<int:comment_id>', views.create_comment_reply),
]
