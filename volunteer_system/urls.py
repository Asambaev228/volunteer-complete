from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from events.views import home

urlpatterns = [
    path('admin/', include('custom_admin.urls')),  # Наша кастомная админка
    path('django-admin/', admin.site.urls),  # Стандартная админка (на случай если заработает)
    path('', home, name='home'),
    path('accounts/', include('accounts.urls')),
    path('events/', include('events.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]