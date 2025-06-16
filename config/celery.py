# Модуль os представляет интерфейс для взаимодействия с операционной системой
# Он позволяет выполнять множество системных операций прямо из Python-кода
import os

# Celery - основной класс для создания celery-приложения
from celery import Celery

# Указать Celery, где искать настройки Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

# Создать celery-приложение с именем config
app = Celery("config")

# Загрузить настройки celery из Django. Те, что начинаются с CELERY_
app.config_from_object("django.conf:settings", namespace="CELERY")

# Автоматически находить и регистрировать задачи во всех приложениях Django
app.autodiscover_tasks()
