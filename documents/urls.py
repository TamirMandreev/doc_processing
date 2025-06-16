from django.urls import path

from documents.apps import DocumentsConfig
from documents.views import DocumentCreateAPIView

app_name = DocumentsConfig.name  # Пространство имен приложения

urlpatterns = [
    path("upload/", DocumentCreateAPIView.as_view(), name="document-upload"),
]
