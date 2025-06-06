# ModelSerializer предназначен для упрощения процесса преобразования моделей Django в формат JSON и обратно
from rest_framework.serializers import ModelSerializer

from users.models import User

# Создать сериализатор
class UserSerializer(ModelSerializer):

    # Внутренний класс Meta служит для отделения конфигурационных данных от логики основного класса
    # Это повышает читаемость и структуру кода
    class Meta:
        model = User # Модель, на основе которой строится сериализатор
        fields = '__all__' # Список полей, которые необходимо сериализовать