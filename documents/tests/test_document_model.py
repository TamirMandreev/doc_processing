import pytest

# SimpleUploadedFile - вспомогательный класс Django для тестирования,
# который имитирует загруженный файл в памяти (без сохранения на диск)
from django.core.files.uploadedfile import SimpleUploadedFile
from django.template.defaultfilters import title

from documents.models import Document
from users.models import User


# Создать простого пользователя
@pytest.fixture
def user():
    return User.objects.create_user(
        email="tamirmandreev@example.com", password="<PASSWORD>"
    )


# Создать файл (фальшивый файл для теста)
@pytest.fixture
def file():
    return SimpleUploadedFile(
        "test_file.pfd",  # Имя файла
        b"file_content",  # Содержимое файла в байтах
        "application/pdf",  # Тип файла
    )


# Протестировать создание документа
@pytest.mark.django_db  # Разрешить доступ к базе данных для этого теста
def test_document_creation(user, file):
    document = Document.objects.create(
        file=file,
        user=user,
    )

    assert document.file is not None
    assert document.status == "pending"
    assert document.user == user
    assert document.uploaded_at is not None
    assert document.processed_at is None
