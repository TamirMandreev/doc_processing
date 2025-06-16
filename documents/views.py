# Generic-классы - это набор готовых представлений (views), которые упрощают создание стандартных CRUD-операций
from rest_framework.generics import CreateAPIView

from documents.serializers import DocumentSerializer
from documents.tasks import send_document_upload_notification


# Create your views here.


# Создать представление для загрузки документа
class DocumentCreateAPIView(CreateAPIView):
    serializer_class = DocumentSerializer

    # Добавить автоматическое заполнение поля user (пользователь, загрузивший документ)
    def perform_create(self, serializer):
        # Сохранить объект в базу данных, заполнив поле user
        serializer.save(user=self.request.user)

        # Отправить администратору уведомление о том, что пользователь загрузил документ
        send_document_upload_notification(self.request.user.email)
