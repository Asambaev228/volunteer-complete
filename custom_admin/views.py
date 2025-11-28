from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from events.models import Event, EventCategory, VolunteerApplication
from events.export_views import export_events_excel, export_categories_excel, export_applications_excel

def is_admin(user):
    """Проверка что пользователь администратор"""
    return user.is_authenticated and user.is_staff

@user_passes_test(is_admin)
def admin_dashboard(request):
    """Главная страница админки"""
    stats = {
        'events_count': Event.objects.count(),
        'categories_count': EventCategory.objects.count(), 
        'applications_count': VolunteerApplication.objects.count(),
        'users_count': Event.objects.values('organizer').distinct().count(),
    }
    return render(request, 'custom_admin/dashboard.html', {'stats': stats})

@user_passes_test(is_admin)
def admin_events(request):
    """Управление мероприятиями"""
    events = Event.objects.all().select_related('category', 'organizer')
    return render(request, 'custom_admin/events.html', {'events': events})

@user_passes_test(is_admin)  
def admin_categories(request):
    """Управление категориями"""
    categories = EventCategory.objects.all()
    return render(request, 'custom_admin/categories.html', {'categories': categories})

@user_passes_test(is_admin)
def admin_applications(request):
    """Управление заявками"""
    applications = VolunteerApplication.objects.all().select_related('volunteer', 'event')
    return render(request, 'custom_admin/applications.html', {'applications': applications})

@user_passes_test(is_admin)
def admin_export(request):
    """Страница экспорта данных"""
    return render(request, 'custom_admin/export.html')