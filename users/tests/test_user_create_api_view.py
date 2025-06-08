import pytest
# reverse получапет URL по имени маршрута
from django.urls import reverse
# status предоставляет удобные константы для HTTP статус-кодов вместо "магических чисел"
from rest_framework import status
# APIClient имитирует HTTP-запросы к API в тестовой среде
from rest_framework.test import APIClient
from users.models import User


# Создать клиент для тестирования API
@pytest.fixture
def api_client():
    return APIClient()

# Создать данные для создания пользователя
@pytest.fixture
def valid_user_data():
    return {
        'email': 'tamirmandreev@example.com',
        'password': '<PASSWORD>',
    }

@pytest.mark.django_db # Разрешить доступ к базе данных для этого теста
def test_user_create_success(api_client, valid_user_data):
    '''
    Тестирует успешное создание пользователя
    :param api_client: клиент для тестирования API
    :param valid_user_data: данные для создания пользователя
    :return:
    '''
    # Получить URL-адрес
    url = reverse('users:register')
    # Выполнить HTTP POST-запрос к API
    response = api_client.post(url, data=valid_user_data, format='json')

    # Проверить статус-код
    assert response.status_code == status.HTTP_201_CREATED
    # Проверить, что создался только один объект
    assert User.objects.count() == 1

    # Получить созданного пользователя
    user = User.objects.first()
    # Проверить его поля
    assert user.email == valid_user_data['email']
    assert user.check_password(valid_user_data['password'])
    # Проверить, что пароль не сохраняется в открытом виде
    assert user.password != valid_user_data['password']
    assert len(user.password) > 30 # Проверка на хэш


@pytest.mark.django_db
def test_user_create_failure(api_client):
    '''
    Тестирует ошибку при создании пользователя
    :param api_client: клиент для тестирования API
    :return:
    '''
    # Получить URL-адрес
    url = reverse('users:register')
    # Создать неверные данные
    invalid_user_data = {
        'email': 'tamir',
        'password': '',
    }
    # Выполнить HTTP POST-запрос к API
    response = api_client.post(url, data=invalid_user_data, format='json')

    # Проверить статус-код
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    # Проверить, что объект не создался
    assert User.objects.count() == 0

    # Проверить, что в ответе API содержается переданные в HTTP запросе поля
    assert 'email' in response.data
    assert 'password' in response.data


@pytest.mark.django_db
def test_user_create_duplicate_email(api_client, valid_user_data):
    '''
    Тестирует уникальность email пользователя
    :param api_client: клиент для тестирования API
    :param valid_user_data: данные для создания пользователя
    :return:
    '''
    # Получить URL-адрес
    url = reverse('users:register')
    # Создать первого пользователя
    api_client.post(url, data=valid_user_data, format='json')
    # Попытаться создать второго пользователя с теми же данными
    response = api_client.post(url, data=valid_user_data, format='json')

    # Проверить статус-код
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    # Проверить, что второй объект не создался
    assert User.objects.count() == 1



