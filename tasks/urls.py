from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from tasks import views

urlpatterns = [
    path('hello-world', views.hello_world),
    path('hello', views.hello),
]
