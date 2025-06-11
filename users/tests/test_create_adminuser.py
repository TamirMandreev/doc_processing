import pytest
# Функция call_command позволяет вызывать management-команды (те, что обычно запускаются через python manage.py ...)
# напрямую из Python-кода
from django.core.management import call_command
# Импортировать настройки проекта
from django.conf import settings

from users.models import User


@pytest.mark.django_db # Разрешить доступ к базе данных для этого теста
def test_create_adminuser():
    # Вызвать команду
    call_command('create_adminuser')

    # Проверить созданного пользователя
    admin = User.objects.get(email=settings.ADMIN_EMAIL)
    assert admin.is_staff is True
    assert admin.is_active is True

