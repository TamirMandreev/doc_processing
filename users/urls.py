from django.urls import path

# TokenObtainPairView - представление для получения пары токенов (access и refresh)
# TokenRefreshView - представление для обновления access токена с помощью refresh токена
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.apps import UsersConfig
from users.views import UserCreateAPIView


app_name = UsersConfig.name # Пространство имен приложения

urlpatterns = [
    path('register/', UserCreateAPIView.as_view(), name='register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

