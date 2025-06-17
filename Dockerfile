# Указать базовый образ для контейнера
FROM python:3.12-slim

# Создать рабочую директорию
WORKDIR /app

# Установить зависимости для PostgreSQL
RUN apt-get update \
    && apt-get install -y gcc libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Скопировать файлы управления зависимостями
COPY pyproject.toml poetry.lock ./

# Установить poetry
RUN pip install poetry

# Отключить создание виртуального окружения Poetry при установке зависимостей
RUN poetry config virtualenvs.create false

# Установить зависимости
RUN poetry install --no-root

# Создать папку для хранения документов
RUN mkdir /app/media

# Скопировать проект
COPY . ./

# Открыть порт 8000 для взаимодействия с приложением
EXPOSE 8000

