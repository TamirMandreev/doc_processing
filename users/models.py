from django.db import models
# AbstractUser - абстрактный класс, который включает все стандартные поля Django-модели User
# BaseUserManager - это класс, который предоставляет основные методы для создания и управления пользователями
from django.contrib.auth.models import AbstractUser, BaseUserManager

# Создать кастомный менеджер для модели User
class UserManager(BaseUserManager):
    # Включить кастомный менеджер модели в миграции базы данных
    use_in_migrations = True

    # Создать приватный метод для создания пользователя
    # Метод не предназначен для прямого вызова извне - только внутри менеджера
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Пользователи должны иметь email')
        # Привести домен email к нижнему регистру
        email = self.normalize_email(email)
        # Создать объект пользователя
        user = self.model(email=email, **extra_fields)
        # Установить пароль
        user.set_password(password)
        # Сохранить в базу данных
        user.save(using=self._db)
        # Вернуть созданный и сохраненный объект пользователя (для дальнейшего использования)
        return user

    # Создать публичный интерфейс для создания обычного (не административного) пользователя
    def create_user(self, email, password=None, **extra_fields):
        # У пользователя по умолчанию нет прав суперпользователя
        extra_fields.setdefault('is_superuser', False)
        # У пользователя по умолчанию нет доступа к административной панели Django
        extra_fields.setdefault('is_staff', False)
        # Создать пользователя через приватный метод
        return self._create_user(email, password, **extra_fields)

    # Создать публичный интерфейс для создания суперпользователя
    def create_superuser(self, email, password, **extra_fields):
        # У пользователя по умолчанию прав суперпользователя
        extra_fields.setdefault('is_superuser', True)
        # У пользователя по умолчанию есть доступ к административной панели Django
        extra_fields.setdefault('is_staff', True)

        # Добавить проверки. Защита от явной передачи False
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Суперпользователь должен иметь is_superuser=True.')
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Суперпользователь должен иметь is_staff=True.')

        # Создать пользователя через приватный метод
        return self._create_user(email, password, **extra_fields)

# Создать кастомную модель пользователя
class User(AbstractUser):
    # Удалить поле username из модели
    username = None
    email = models.EmailField(unique=True, verbose_name="Email", help_text="Укажите email")

    # Использовать поле email в качестве уникального идентификатора пользователя (вместо стандартного username)
    USERNAME_FIELD = "email"
    # Определить список полей, которые будут запрашиваться при создании пользователя через команду createsuperuser
    REQUIRED_FIELDS = []

    # Создать и назначить менеджер модели
    # Он отвечает за все взаимодействия с базой данных для этой модели
    objects = UserManager()

    # Определить строкое представление пользователя
    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'