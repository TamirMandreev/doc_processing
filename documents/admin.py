from django.contrib import admin

from documents.models import Document

# Зарегистрировать модель Document в панели администратора
@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    # Отобразить в списке пользователей следующие поля
    list_display = ('title',)