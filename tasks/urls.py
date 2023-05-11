from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from tasks import views

urlpatterns = [
    path('hello-world', views.hello_world),
    path('hello', views.hello),
    path('sign-up', views.sign_up),
    path('token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('task', views.create_task),
    path('task/<int:task_id>', views.edit_delete_task),
]
