import pytest

# Функция call_command позволяет вызывать management-команды (те, что обычно запускаются через python manage.py ...)
# напрямую из Python-кода
from django.core.management import call_command

# Импортировать настройки проекта
from django.conf import settings

from users.models import User, UserManager
from users.tests.test_user_model import superuser


@pytest.fixture
def user_manager():
    """
    Создает менеджер для модели User
    :return:
    """
    # Создать экземпляр менеджера
    manager = UserManager()
    # Установить модель, с которой будет работать менеджер
    manager.model = User
    # Вернуть менеджер
    return manager


@pytest.mark.django_db  # Разрешить доступ к базе данных для этого теста
def test_create_adminuser(capsys):
    """
    Тестирует создание администратора
    :param capsys: Фикустура, которая перехватывает все, что программа выводит в консоль
    :return:
    """
    # Убедиться, что админ не существует
    User.objects.filter(email=settings.ADMIN_EMAIL).delete()

    # Вызвать команду
    call_command("create_adminuser")

    # Проверить созданного пользователя
    admin = User.objects.get(email=settings.ADMIN_EMAIL)
    assert admin.is_staff is True
    assert admin.is_active is True

    captured = capsys.readouterr()
    assert f"Администратор {settings.ADMIN_EMAIL} создан" in captured.out


@pytest.mark.django_db  # Разрешить доступ к базе данных для этого теста
def test_create_adminuser_when_admin_exists(capsys):
    """
    Тестирует создание администратора, когда администратор уже есть
    :param capsys: Фикустура, которая перехватывает все, что программа выводит в консоль
    :return:
    """

    # Создать администратора
    User.objects.create(
        email=settings.ADMIN_EMAIL,
        password=settings.ADMIN_PASSWORD,
        is_staff=True,
    )
    # Вызвать команду
    call_command("create_adminuser")

    # Перехватить вывод
    captured = capsys.readouterr()
    assert f"Администратор {settings.ADMIN_EMAIL} уже существует!" in captured.out


@pytest.mark.django_db  # Разрешить доступ к базе данных для этого теста
def test_create_user_without_email(user_manager):
    """
    Тестирует создание пользователя без email
    :param user_manager: менеджер модели User
    :return:
    """

    # В следующем блоке кода должно произойти исключение ValueError
    with pytest.raises(ValueError) as excinfo:
        user_manager.create_user(email=None)

    assert "Пользователи должны иметь email" in str(excinfo.value)


@pytest.mark.django_db  # Разрешить доступ к базе данных для этого теста
def test_create_superuser_without_staff_flag(user_manager):
    """
    Тестирует создание суперпользователя без указания is_superuser=True
    :return:
    """

    with pytest.raises(ValueError) as excinfo:
        user_manager.create_superuser(
            email="superuser@example.com", password=12345, is_staff=False
        )

    assert "Суперпользователь должен иметь is_staff=True" in str(excinfo.value)


@pytest.mark.django_db  # Разрешить доступ к базе данных для этого теста
def test_create_superuser_without_superuser_flag(user_manager):
    """
    Тестирует создание суперпользователя без указания is_superuser=True, is_staff=True
    :return:
    """

    with pytest.raises(ValueError) as excinfo:
        user_manager.create_superuser(
            email="superuser@example.com", password=12345, is_superuser=False
        )

    assert "Суперпользователь должен иметь is_superuser=True" in str(excinfo.value)
