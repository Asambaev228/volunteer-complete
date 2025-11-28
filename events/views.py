from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Event, VolunteerApplication, EventCategory

def home(request):
    """Главная страница"""
    return render(request, 'home.html')

def event_list(request):
    """
    Список всех активных мероприятий.
    ДОСТУПНО ВСЕМ (гостевой доступ без авторизации)
    """
    events = Event.objects.filter(status='active').order_by('event_date')
    return render(request, 'events/event_list.html', {'events': events})

def event_detail(request, event_id):
    """
    Детальная страница мероприятия.
    Гости могут просматривать, но не могут подавать заявки.
    """
    event = get_object_or_404(Event, id=event_id)
    user_application = None
    
    # Проверяем заявку только для авторизованных пользователей
    if request.user.is_authenticated:
        user_application = VolunteerApplication.objects.filter(
            volunteer=request.user, 
            event=event
        ).first()
    
    return render(request, 'events/event_detail.html', {
        'event': event,
        'user_application': user_application
    })

@login_required
def apply_for_event(request, event_id):
    """
    Подача заявки на мероприятие.
    ТОЛЬКО ДЛЯ ЗАРЕГИСТРИРОВАННЫХ ПОЛЬЗОВАТЕЛЕЙ
    """
    event = get_object_or_404(Event, id=event_id)
    
    # Проверяем нет ли уже заявки от этого пользователя
    existing_application = VolunteerApplication.objects.filter(
        volunteer=request.user, 
        event=event
    ).first()
    
    if existing_application:
        messages.warning(request, 'Вы уже подавали заявку на это мероприятие!')
    else:
        # Создаем новую заявку
        application = VolunteerApplication.objects.create(
            volunteer=request.user,
            event=event,
            status='pending',
            message=f'Заявка от пользователя {request.user.username}'
        )
        messages.success(request, 'Заявка успешно подана! Ожидайте подтверждения организатором.')
    
    return redirect('event_detail', event_id=event_id)

def event_search(request):
    """
    Поиск и фильтрация мероприятий.
    ДОСТУПНО ВСЕМ (гостевой доступ без авторизации)
    """
    query = request.GET.get('q', '')  # Поисковый запрос
    category_id = request.GET.get('category', '')  # Фильтр по категории
    
    # Начинаем с активных мероприятий
    events = Event.objects.filter(status='active')
    
    # Поиск по названию и описанию (безопасно через Django ORM)
    if query:
        events = events.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )
    
    # Фильтрация по категории
    if category_id:
        events = events.filter(category_id=category_id)
    
    # Получаем все категории для фильтра
    categories = EventCategory.objects.all()
    
    return render(request, 'events/event_search.html', {
        'events': events,
        'query': query,
        'categories': categories,
        'selected_category': category_id,
    })