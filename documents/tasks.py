# Импортировать настройки Django
from celery import shared_task

# Импортировать настройки проекта
from django.conf import settings

# send_mail отправляет электронное письмо с использованием настроек почтового сервера, указанных в settings.py
from django.core.mail import send_mail


# Декоратор @shared_task используется в Celery для создания асинхронных задач,
# которые могут выполняться в фоновом режиме вне Django-приложения
@shared_task
def send_document_upload_notification(user_email):
    """
    Отправляет администратору уведомление о том, что пользователь загрузил документ
    :param user_email: адрес электронной почты пользователя
    :return:
    """
    send_mail(
        subject="Загружен новый документ",  # Тема письма
        message=f"Пользователь {user_email} загрузил документ",  # Содержимое письма
        from_email=settings.EMAIL_HOST_USER,  # Email отправителя
        recipient_list=[settings.ADMIN_EMAIL],  # Email получателя (администратора)
    )


# Декоратор @shared_task используется в Celery для создания асинхронных задач,
# которые могут выполняться в фоновом режиме вне Django-приложения
@shared_task
def send_document_confirmation_notification(user_email, admin_comment):
    """
    Отправляет пользователю уведомление о том, что администратор подтвердил загруженный документ
    :param user_email: адрес электронной почты пользователя
    :param admin_comment: комментарий администратора
    :return:
    """
    send_mail(
        subject="Документ подтвержден",  # Тема письма
        message=admin_comment,  # Содержимое письма
        from_email=settings.EMAIL_HOST_USER,  # Email отправителя
        recipient_list=[user_email],  # Email получателя
    )


# Декоратор @shared_task используется в Celery для создания асинхронных задач,
# которые могут выполняться в фоновом режиме вне Django-приложения
@shared_task
def send_document_rejection_notification(user_email, admin_comment):
    """
    Отправляет пользователю уведомление о том, что администратор отклонил загруженный документ
    :param user_email: адрес электронной почты пользователя
    :param admin_comment: комментарий администратора
    :return:
    """
    send_mail(
        subject="Документ отклонен",  # Тема письма
        message=admin_comment,  # Содержимое письма
        from_email=settings.EMAIL_HOST_USER,  # Email отправителя
        recipient_list=[user_email],  # Email получателя
    )
