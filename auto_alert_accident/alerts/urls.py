from django.urls import path
from . import views

urlpatterns = [
    path('', views.emergency_page, name='home'),
    path('emergency/', views.emergency_page, name='emergency_page'),
    path('save-alert/', views.save_alert, name='save_alert'),
    path('map/', views.map_dashboard, name='map_dashboard'),
]
