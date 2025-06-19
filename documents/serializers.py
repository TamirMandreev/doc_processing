# ModelSerializer предназначен для упрощения процесса преобразования моделей Django в формат JSON и обратно
from rest_framework.serializers import ModelSerializer

from documents.models import Document


class DocumentSerializer(ModelSerializer):
    class Meta:
        model = Document
        fields = ['id', 'file']

