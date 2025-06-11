# Импортировать настройки Django
from celery import shared_task
from django.conf import settings
# send_mail отправляет электронное письмо с использованием настроек почтового сервера, указанных в settings.py
from django.core.mail import send_mail

# Декоратор @shared_task используется в Celery для создания асинхронных задач,
# которые могут выполняться в фоновом режиме вне Django-приложения
@shared_task
def send_document_upload_notification(user_email):
    '''
    Отправляет администратору уведомление о том, что пользователь загрузил документ
    :param admin_email: адрес электронной почты администратора
    :return:
    '''
    send_mail(
        subject='Загружен новый документ', # Тема письма
        message=f'Пользователь {user_email} загрузил документ', # Содержимое письма
        from_email=settings.EMAIL_HOST_USER, # Email отправителя
        recipient_list=[settings.ADMIN_EMAIL], # Email получателя (администратора)
    )

