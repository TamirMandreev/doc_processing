import pytest

# Класс AdminSite - базовый административный интерфейс Django
from django.contrib.admin import AdminSite

# Декоратор patch используется для временной замены (мокинга) объектов во время тестирования
from unittest.mock import patch, MagicMock

# RequestFactory создает "фейковый" HTTP-запрос
from django.test import RequestFactory

from documents.admin import DocumentAdmin
from documents.models import Document
from users.models import User


@pytest.fixture
def document_admin():
    """
    Создает фейковый административный интерфейс (с DocumentAdmin)
    :return:
    """
    return DocumentAdmin(Document, AdminSite())


@pytest.fixture
def admin_user():
    """
    Создает администратора
    :return:
    """
    return User.objects.create(email="testuser@example.com", is_staff=True)


@pytest.mark.django_db  # Разрешить доступ к базе данных для этого теста
@patch(
    "documents.tasks.send_document_confirmation_notification.delay"
)  # Подменить функцию
@patch(
    "documents.tasks.send_document_rejection_notification.delay"
)  # Подменить функцию
def test_save_model(mock_reject_task, mock_confirm_task, document_admin, admin_user):
    """
    Тестирует отправку уведомлений об отклонении или подтверждении документа
    :param mock_reject_task: фейковая celery-задача отправки уведомления об отклонении документа
    :param mock_confirm_task: фейковая celery-задача отправки уведомления о подтверждении документа
    :param document_admin: фейковый административный интерфейс (с DocumentAdmin)
    :param admin_user: администратор
    :return:
    """
    # Создать тестовый документ
    document = Document.objects.create(
        title="Test Document", file="test.pdf", user=admin_user
    )

    # Создать "фейковую" (поддельную) форму Django
    form = MagicMock()
    # Задать атрибут changed_data для мок-формы
    # Если в админке Django изменить только поле status и нажать "сохранить", то changed_data будет ['status']
    form.changed_data = ["status"]
    # Изменить поле status. Админка должна среагировать на это изменение
    document.status = "approved"
    # Вызвать метод save_model в тестовом административном интерефейсе
    document_admin.save_model(admin_user, document, form, True)

    # Проверить, что поле processed_at заполнилось
    assert document.processed_at is not None
    # Проверить отправку уведомления подтверждения документа
    mock_confirm_task.assert_called_once_with(
        document.user.email, document.admin_comment
    )

    # Изменить поле status. Админка должна среагировать на это изменение
    document.status = "rejected"
    # Вызвать метод save_model в тестовом административном интерефейсе
    document_admin.save_model(admin_user, document, form, True)

    # Проверить, что поле processed_at заполнилось
    assert document.processed_at is not None
    # Проверить отправку уведомления подтверждения документа
    mock_reject_task.assert_called_once_with(
        document.user.email, document.admin_comment
    )


@pytest.mark.django_db  # Разрешить доступ к базе данных этому тесту
def test_permissions(document_admin, admin_user):
    """
    Тестирует права доступа к модели Document в панели администратора
    :param document_admin: фейковый административный интерфейс (с DocumentAdmin)
    :param admin_user: администратор
    :return:
    """
    # Создать "фейковый HTTP-запрос, который имитирует реальный запрос к админке
    request = RequestFactory().get("/")
    # Подставить тестового пользователя
    request.user = admin_user

    # Тестирование has_view_permission
    assert document_admin.has_view_permission(request) is True
    # Тестирование has_change_permission
    assert document_admin.has_change_permission(request) is True
    # Тестирование has_module_permission
    assert document_admin.has_module_permission(request) is True
