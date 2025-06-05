from django.db import models
# AbstractUser - абстрактный класс, который включает все стандартные поля Django-модели User
from django.contrib.auth.models import AbstractUser

# Создать кастомную модель пользователя
class User(AbstractUser):
    # Удалить поле username из модели
    username = None
    email = models.EmailField(unique=True, verbose_name="Email", help_text="Укажите email")

    # Использовать поле email в качестве уникального идентификатора пользователя (вместо стандартного username)
    USERNAME_FIELD = "email"
    # Определить список полей, которые будут запрашиваться при создании пользователя через команду createsuperuser
    REQUIRED_FIELDS = []

    # Определить строкое представление пользователя
    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'