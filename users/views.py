# Generic-классы - это набор готовых представлений (views), которые упрощают создание стандартных CRUD-операций
# для моделей Django
from rest_framework.generics import CreateAPIView

# Импортировать модель пользователя
from users.models import User
# Импортировать сериализатор
from users.serializers import UserSerializer

# Создать представление для регистрации пользователя
class UserCreateAPIView(CreateAPIView):
    # Указать сериализатор
    serializer_class = UserSerializer

