from django.db import models

from users.models import User


# Create your models here.


# Создать модель для хранения загруженных файлов
class Document(models.Model):
    # 1-й элемент кортежа - значение, хранимое в базе данных
    # 2-й элемент кортежа - человекочитаемое описание, отображаемое в админке и формах
    STATUS_CHOICES = [
        ("pending", "На рассмотрении"),
        ("approved", "Подтвержден"),
        ("rejected", "Отклонен"),
    ]

    # Название документа
    title = models.CharField(max_length=255)
    # В этом поле будет храниться путь к файлу (документу)
    file = models.FileField(upload_to="documents/")
    # Статус документа
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")
    # Комментарий администратора
    admin_comment = models.TextField(blank=True, null=True)
    # Пользователь, загрузивший документ
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    # Дата и время загрузки документа
    uploaded_at = models.DateTimeField(auto_now_add=True)
    # Дата и время обработки документа
    processed_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"

    class Meta:
        verbose_name = "Документ"
        verbose_name_plural = "Документы"
