from django.urls import path
from . import views
from events.export_views import export_events_excel, export_categories_excel, export_applications_excel

urlpatterns = [
    path('', views.admin_dashboard, name='admin_dashboard'),
    path('events/', views.admin_events, name='admin_events'),
    path('categories/', views.admin_categories, name='admin_categories'),
    path('applications/', views.admin_applications, name='admin_applications'),
    path('export/', views.admin_export, name='admin_export'),
    path('export/events/', export_events_excel, name='admin_export_events'),
    path('export/categories/', export_categories_excel, name='admin_export_categories'),
    path('export/applications/', export_applications_excel, name='admin_export_applications'),
    path('events/create/', views.create_event, name='admin_create_event'),
]