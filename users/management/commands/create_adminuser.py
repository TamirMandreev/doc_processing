# Кастомные управляющие команды создаются через класс BaseCommand
from django.core.management import BaseCommand

# Импортировать настройки проекта
from django.conf import settings

from users.models import User


# Создать команду для создания администратора
class Command(BaseCommand):
    # Основная логика команды находится в методе handle
    def handle(self, *args, **options):
        # Проверить, не существует ли администратор уже
        if not User.objects.filter(email=settings.ADMIN_EMAIL).exists():
            # Создать администратора
            user = User.objects.create(email=settings.ADMIN_EMAIL)
            user.is_staff = True
            user.is_active = True
            user.set_password(settings.ADMIN_PASSWORD)
            user.save()
            self.stdout.write(
                self.style.SUCCESS(f"Администратор {settings.ADMIN_EMAIL} создан!")
            )
        else:
            self.stdout.write(
                self.style.WARNING(
                    f"Администратор {settings.ADMIN_EMAIL} уже существует!"
                )
            )
