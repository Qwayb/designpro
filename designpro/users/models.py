from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class DesignRequest(models.Model):
    STATUS_CHOICES = (
        ('Новая', 'Новая'),
        ('Принято в работу', 'Принято в работу'),
        ('Выполнено', 'Выполнено'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    image = models.ImageField(upload_to='design_requests/', validators=[

        FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'bmp'])
    ])
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Новая')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title