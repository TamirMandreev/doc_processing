# Generic-классы - это набор готовых представлений (views), которые упрощают создание стандартных CRUD-операций
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.response import Response

from documents.models import Document
from documents.serializers import DocumentSerializer
from documents.tasks import send_document_upload_notification


# Create your views here.


# Создать представление для загрузки документа
class DocumentCreateAPIView(CreateAPIView):
    serializer_class = DocumentSerializer

    # При загрузке документа пользователь в ответ получает id созданной записи в БД
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(
            {'id': serializer.instance.id},
            status=status.HTTP_201_CREATED,
            headers=headers
        )

    # Добавить автоматическое заполнение поля user (пользователь, загрузивший документ)
    def perform_create(self, serializer):
        # Сохранить объект в базу данных, заполнив поле user
        serializer.save(user=self.request.user)

        # Отправить администратору уведомление о том, что пользователь загрузил документ
        send_document_upload_notification(self.request.user.email)


# Создать представление для просмотра списка документов
class DocumentListAPIView(ListAPIView):
    serializer_class = DocumentSerializer

    # Пользовать видит только свои документы со статусо "Подтвержден"
    def get_queryset(self):
        documents = Document.objects.filter(user=self.request.user, status='approved')
        return documents