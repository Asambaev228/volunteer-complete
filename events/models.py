from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from volunteer_system.models import TimeStampedModel

class EventCategory(TimeStampedModel):
    """Категории мероприятий (экология, социальная помощь и т.д.)"""
    name = models.CharField(max_length=100, verbose_name='Название категории')
    description = models.TextField(blank=True, verbose_name='Описание')
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Категория мероприятия'
        verbose_name_plural = 'Категории мероприятий'

class Event(TimeStampedModel):
    """Мероприятия, на которые можно подавать заявки"""
    STATUS_CHOICES = (
        ('draft', 'Черновик'),
        ('active', 'Активно'),
        ('completed', 'Завершено'),
        ('cancelled', 'Отменено'),
    )
    
    title = models.CharField(max_length=200, verbose_name='Название мероприятия')
    description = models.TextField(verbose_name='Описание')
    category = models.ForeignKey(EventCategory, on_delete=models.CASCADE, verbose_name='Категория')
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='organized_events', verbose_name='Организатор')
    event_date = models.DateTimeField(verbose_name='Дата и время мероприятия')
    location = models.CharField(max_length=200, verbose_name='Место проведения')
    required_volunteers = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)], verbose_name='Требуемое количество волонтеров')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft', verbose_name='Статус')
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Мероприятие'
        verbose_name_plural = 'Мероприятия'
        ordering = ['-event_date']

class VolunteerApplication(TimeStampedModel):
    """Заявки пользователей на участие в мероприятиях"""
    STATUS_CHOICES = (
        ('pending', 'На рассмотрении'),
        ('approved', 'Одобрено'),
        ('rejected', 'Отклонено'),
        ('cancelled', 'Отменено волонтером'),
    )
    
    volunteer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='volunteer_applications', verbose_name='Волонтер')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='volunteer_applications', verbose_name='Мероприятие')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='Статус заявки')
    message = models.TextField(blank=True, verbose_name='Сообщение волонтера')
    
    def __str__(self):
        return f"{self.volunteer.username} - {self.event.title}"
    
    class Meta:
        verbose_name = 'Заявка волонтера'
        verbose_name_plural = 'Заявки волонтеров'
        unique_together = ['volunteer', 'event']  # Один пользователь - одна заявка на мероприятие