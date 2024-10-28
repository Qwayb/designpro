from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator

class Category(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Название категории',
        error_messages={
            'unique': 'Категория с таким названием уже существует',
        }
    )

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        DesignRequest.objects.filter(category=self).delete()
        super().delete(*args, **kwargs)

class DesignRequest(models.Model):
    STATUS_CHOICES = (
        ('Новая', 'Новая'),
        ('Принято в работу', 'Принято в работу'),
        ('Выполнено', 'Выполнено'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, verbose_name='Категория')
    image = models.ImageField(upload_to='design_requests/', validators=[
        FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'bmp'])
    ], verbose_name='Изображение')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Новая', verbose_name='Статус')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    design_image = models.ImageField(upload_to='designs/', validators=[
        FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'bmp'])
    ], null=True, blank=True, verbose_name='Изображение дизайна')
    comment = models.TextField(null=True, blank=True, verbose_name='Комментарий')

    def __str__(self):
        return self.title