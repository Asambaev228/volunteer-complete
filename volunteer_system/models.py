from django.db import models

class TimeStampedModel(models.Model):
    """
    Абстрактная базовая модель с полями created_at и updated_at.
    Все основные модели наследуются от этой модели.
    """
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        abstract = True