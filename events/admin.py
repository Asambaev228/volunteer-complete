from django.contrib import admin
from .models import EventCategory, Event, VolunteerApplication

# Минимальные админ-классы без сложных функций
@admin.register(EventCategory)
class EventCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'event_date', 'status']
    list_filter = ['status', 'category']
    search_fields = ['title', 'description']

@admin.register(VolunteerApplication)
class VolunteerApplicationAdmin(admin.ModelAdmin):
    list_display = ['volunteer', 'event', 'status', 'created_at']
    list_filter = ['status']
    search_fields = ['volunteer__username', 'event__title']