from django.urls import path
from . import views
from .export_views import export_events_excel

urlpatterns = [
    path('', views.event_list, name='event_list'),
    path('search/', views.event_search, name='event_search'),
    path('<int:event_id>/', views.event_detail, name='event_detail'),
    path('<int:event_id>/apply/', views.apply_for_event, name='apply_for_event'),
    path('export/excel/', export_events_excel, name='export_events_excel'),
]