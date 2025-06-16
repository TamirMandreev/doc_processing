import pytest

from users.models import User


# Создать простого пользователя
@pytest.fixture
def user():
    return User.objects.create_user(
        email="tamirmandreev@example.com",
        password="<PASSWORD>",
    )


# Создать суперпользователя
@pytest.fixture
def superuser():
    return User.objects.create_superuser(
        email="tamirmandreev@example.com",
        password="<PASSWORD>",
    )


# Протестировать создание простого пользователя
@pytest.mark.django_db  # Разрешаем доступ к базе данных для этого теста
def test_user_creation(user):
    assert user.email == "tamirmandreev@example.com"
    assert user.password != "<PASSWORD>"  # Пароль захэширован
    assert user.is_active == True
    assert user.is_staff == False
    assert user.is_superuser == False
    assert str(user) == "tamirmandreev@example.com"


# Протестировать создание суперпользователя
@pytest.mark.django_db  # Разрешаем доступ к базе данных для этого теста
def test_superuser_creation(superuser):
    assert superuser.email == "tamirmandreev@example.com"
    assert superuser.password != "<PASSWORD>"  # Пароль захэширован
    assert superuser.is_active == True
    assert superuser.is_staff == True
    assert superuser.is_superuser == True
    assert str(superuser) == "tamirmandreev@example.com"
