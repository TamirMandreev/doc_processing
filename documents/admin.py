from django.contrib import admin
from django.utils import timezone

from documents.models import Document
from documents.tasks import (
    send_document_confirmation_notification,
    send_document_rejection_notification,
)


# Зарегистрировать модель Document в панели администратора
@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    # Отобразить в списке пользователей следующие поля
    list_display = (
        "pk",
        "user",
        "file",
        "uploaded_at",
        "processed_at",
        "status",
    )
    # Добавить фильтрацию по полям
    list_filter = ("status", "uploaded_at")

    # Определить, какие поля будут отображаться в форме
    def get_fields(self, request, obj=None):
        return [
            "user",
            "file",
            "admin_comment",
            "uploaded_at",
            "processed_at",
            "status",
        ]

    # Определить поля только для чтения
    def get_readonly_fields(self, request, obj=None):
        return ["user", "file", "uploaded_at", "processed_at"]

    # Переопределить метод сохранения объекта
    def save_model(self, request, obj, form, change):
        if change:
            obj.processed_at = timezone.now()
        super().save_model(request, obj, form, change)
        # Если статус изменился на 'approved'
        if change and "status" in form.changed_data and obj.status == "approved":
            send_document_confirmation_notification.delay(
                obj.user.email, obj.admin_comment
            )
        # Если статус изменился на 'rejected'
        elif change and "status" in form.changed_data and obj.status == "rejected":
            send_document_rejection_notification.delay(
                obj.user.email, obj.admin_comment
            )

    # Определить права доступа к модели Document
    def has_view_permission(self, request, obj=None):
        return request.user.is_staff

    def has_change_permission(self, request, obj=None):
        return request.user.is_staff

    def has_module_permission(self, request, obj=None):
        return request.user.is_staff
