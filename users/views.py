# Generic-классы - это набор готовых представлений (views), которые упрощают создание стандартных CRUD-операций
# для моделей Django
from rest_framework.generics import CreateAPIView

# AllowAny разрешает доступ к API всем пользователям, включая анонимных (неаутентифицированных)
from rest_framework.permissions import AllowAny

# Импортировать сериализатор
from users.serializers import UserSerializer


# Создать представление для регистрации пользователя
class UserCreateAPIView(CreateAPIView):
    # Указать сериализатор
    serializer_class = UserSerializer
    # Сделать API-эндпоинт доступным всем пользователям
    permission_classes = [AllowAny]

    # Переопределить стандартное поведение при создании новых объектов
    def perform_create(self, serializer):
        # Создать новый объект в базе данных
        user = serializer.save(is_active=True)
        # Захэшировать пароль
        user.set_password(user.password)
        # Сохранить пользователя с захешированным паролем
        user.save()
