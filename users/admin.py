from django.contrib import admin

from users.models import User

# Зарегистрировать модель User в панели администратора
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    # Отобразить в списке пользователей следующие поля
    list_display = ('email',)