from django.urls import path

from users.apps import UsersConfig
from users.views import UserCreateAPIView


app_name = UsersConfig.name # Пространство имен приложения

urlpatterns = [
    path('register/', UserCreateAPIView.as_view(), name='register'),
]