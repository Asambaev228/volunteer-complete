from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User
from events.models import EventCategory, Event, VolunteerApplication

class Command(BaseCommand):
    help = 'Создает тестовые данные для волонтерской системы'

    def handle(self, *args, **options):
        self.stdout.write('🎯 Создание тестовых данных для волонтерской системы...')
        
        # Создаем тестовых пользователей
        test_users = [
            {'username': 'volunteer1', 'email': 'volunteer1@example.com', 'password': 'password123'},
            {'username': 'volunteer2', 'email': 'volunteer2@example.com', 'password': 'password123'},
            {'username': 'organizer1', 'email': 'organizer1@example.com', 'password': 'password123'},
        ]
        
        for user_data in test_users:
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults={'email': user_data['email']}
            )
            if created:
                user.set_password(user_data['password'])
                user.save()
                self.stdout.write(self.style.SUCCESS(f'✅ Создан пользователь: {user_data["username"]} / {user_data["password"]}'))
        
        # Создаем категории мероприятий
        categories_data = [
            ('Экология', 'Мероприятия по защите окружающей среды и уборке территорий'),
            ('Социальная помощь', 'Помощь пожилым людям, детям и нуждающимся'),
            ('Образование', 'Образовательные мероприятия и мастер-классы'),
            ('Культура', 'Культурные события и мероприятия'),
        ]
        
        categories = {}
        for name, description in categories_data:
            category, created = EventCategory.objects.get_or_create(
                name=name,
                defaults={'description': description}
            )
            categories[name] = category
            if created:
                self.stdout.write(self.style.SUCCESS(f'✅ Создана категория: {name}'))
        
        # Создаем мероприятия
        admin_user = User.objects.get(username='admin')
        
        events_data = [
            {
                'title': 'Уборка городского парка',
                'description': 'Ежегодная весенняя уборка центрального городского парка. Приглашаем всех желающих помочь сделать наш город чище!',
                'category': categories['Экология'],
                'organizer': admin_user,
                'event_date': timezone.now() + timedelta(days=7),
                'location': 'Центральный городской парк',
                'required_volunteers': 25,
                'status': 'active'
            },
            {
                'title': 'Помощь пожилым людям',
                'description': 'Развозка продуктов и лекарств пожилым людям, которые не могут выйти из дома.',
                'category': categories['Социальная помощь'],
                'organizer': admin_user,
                'event_date': timezone.now() + timedelta(days=3),
                'location': 'Центр города, старт от главной площади',
                'required_volunteers': 15,
                'status': 'active'
            },
            {
                'title': 'Мастер-класс по программированию для детей',
                'description': 'Бесплатный мастер-класс по основам программирования для детей от 10 до 14 лет.',
                'category': categories['Образование'],
                'organizer': admin_user,
                'event_date': timezone.now() + timedelta(days=14),
                'location': 'Городская библиотека, компьютерный класс',
                'required_volunteers': 8,
                'status': 'active'
            },
        ]
        
        for event_data in events_data:
            event, created = Event.objects.get_or_create(
                title=event_data['title'],
                defaults=event_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'✅ Создано мероприятие: {event_data["title"]}'))
        
        # Создаем тестовые заявки
        volunteer1 = User.objects.get(username='volunteer1')
        sample_events = Event.objects.filter(status='active')[:2]
        
        for event in sample_events:
            application, created = VolunteerApplication.objects.get_or_create(
                volunteer=volunteer1,
                event=event,
                defaults={
                    'status': 'pending',
                    'message': f'Хочу помочь в мероприятии "{event.title}"'
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'✅ Создана заявка для {volunteer1.username} на {event.title}'))
        
        self.stdout.write(self.style.SUCCESS('\n🎉 Тестовые данные успешно созданы!'))
        self.stdout.write(f'\n📊 Статистика:')
        self.stdout.write(f'   👤 Пользователей: {User.objects.count()}')
        self.stdout.write(f'   🏷️ Категорий: {EventCategory.objects.count()}')
        self.stdout.write(f'   📅 Мероприятий: {Event.objects.count()}')
        self.stdout.write(f'   📝 Заявок: {VolunteerApplication.objects.count()}')
        
        self.stdout.write('\n🔑 Тестовые аккаунты:')
        self.stdout.write('   👑 Администратор: admin / admin123')
        self.stdout.write('   👤 Волонтер 1: volunteer1 / password123')
        self.stdout.write('   🎯 Организатор: organizer1 / password123')