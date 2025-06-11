# Модуль os представляет интерфейс для взаимодействия с операционной системой
# Он позволяет выполнять множество системных операций прямо из Python-кода
import os

# Класс timedelta используется для работы с промежутками времени
# Объект этого класса представляет длительность (разницу между двумя датами или временем)
from datetime import timedelta

from django.conf.global_settings import MEDIA_URL, MEDIA_ROOT
# Функция load_dotenv используется для загрузки переменных окружения из файла .env
# в текущее окружения Python
from dotenv import load_dotenv

# pathlib.Path - это современная замена os.path
# Он делает работу с файловой системой более удобной и безопасной
from pathlib import Path

# Загрузить переменные из .env
# override - перезаписать ли существующие перменные окружения
load_dotenv(override=True)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = []


# Application definition

# Список INSTALLED_APPS определяет, какие приложения Django будут активны в проекте
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework', # Подключить Django REST Framework
    'rest_framework_simplejwt', # Подключить JWT-аутентификацию
    'users', # Подключить приложение users
    'documents', # Подключить приложение documents

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Указать основную модель пользователя в проекте
AUTH_USER_MODEL = 'users.User'

# REST_FRAMEWORK - словарь настроек Django REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication', # По умолчанию используется JWT-аутентификация
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated', # По умолчанию для доступа к API-эндпоинтам пользователь должен быть аутентифицирован
    ]
}

# Настроить время жизни JWT-токенов
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=7), # Срок жизни access token
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7), # Срок жизни refresh token
}

# URL-адрес, по которому будут доступны документы
MEDIA_URL = '/media/'
# Абсолютный путь к директории на сервере, где Django будет сохранять загруженные пользователями файлы
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Использовать часой пояс Django-проекта
CELERY_TIMEZONE = TIME_ZONE
# Фиксировать время начала задачи
CELERY_TASK_TRACK_STARTED = True
# Автоматически прерывать задачи, выполняющиеся более 30 минут
CELERY_TASK_TIME_LIMIT = 30 * 60
# URL Redis-сервера, который Celery будет использовать как очередь задач
CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL')
# URL Redis-сервера для хранения результатов выполненных задач
CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND')

# Настройки почты mail.ru
# Использовать SMTP-сервер для отправки email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend' # django.core.mail.backends.console.EmailBackend
EMAIL_HOST = os.getenv('EMAIL_HOST') # Сервер для отправки email
EMAIL_PORT = os.getenv('EMAIL_PORT') # Порт
EMAIL_USE_SSL = os.getenv('EMAIL_USE_SSL') == 'True' # Должно ли SMTP-соединение использовать SSL-шифрование (True или False)
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER') # Email для аутентификации на SMTP-сервере
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD') # Пароль внешнего приложения для аутентификации на SMTP-сервере
ADMIN_EMAIL = os.getenv('ADMIN_EMAIL') # Email администратора (туда будут приходиться уведомления о загрузке документов)
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD') # Пароль для входа в учетную запись администратора внутри текущего приложения