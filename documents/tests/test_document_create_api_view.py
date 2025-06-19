import pytest

# reverse получает URL по имени маршрута
from django.urls import reverse

# status предоставляет удобные константы для HTTP статус-кодов вместо "магических чисел"
from rest_framework import status

# APIClient имитирует HTTP-запросы к API в тестовой среде
from rest_framework.test import APIClient
from documents.models import Document

# Импоритровать фикстуры из файла с тестами модели Document
from documents.tests.test_document_model import user, file


# Создать клиент для тестирования API
@pytest.fixture
def api_client():
    return APIClient()


# Создать данные для создания документа
@pytest.fixture
def valid_document_data(file, user):
    return {"title": "test_document", "file": file}


@pytest.mark.django_db  # Разрешить доступ к базе данных для этого теста
def test_document_create_success(api_client, valid_document_data, user):
    """
    Тестирует успешное создание документа
    :param api_client: клиент для тестирования API
    :param valid_document_data: данные для создания документа
    :param user: пользователь
    :return:
    """
    # Получить URL-адрес
    url = reverse("documents:document-upload")
    # Авторизовать пользователя
    api_client.force_authenticate(user=user)
    # Выполнить HTTP POST-запрос к API
    response = api_client.post(url, data=valid_document_data, format="multipart")

    # Проверить статус-код
    assert response.status_code == status.HTTP_201_CREATED
    # Проверить, что создался только один объект
    assert Document.objects.count() == 1

    # Проверить созданный документ
    document = Document.objects.first()
    assert document.file is not None
    assert document.status == "pending"
    assert document.admin_comment is None
    assert document.user == user
    assert document.uploaded_at is not None
    assert document.processed_at is None


@pytest.mark.django_db  # Разрешить доступ к базе данных для этого теста
def test_document_create_unauthorized(api_client, valid_document_data):
    """
    Тестирует ошибку 401 Unauthorized
    :param api_client: клиент для тестирования API
    :param valid_document_data: данные для создания документа
    :return:
    """
    # Получить URL-адрес
    url = reverse("documents:document-upload")
    # Выполнить HTTP POST-запрос к API
    response = api_client.post(url, data=valid_document_data, format="multipart")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
