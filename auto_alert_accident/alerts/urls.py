from django.urls import path
from . import views
from .views import create_user

urlpatterns = [

    path("", views.user_login),   # default page

    path("login/", views.user_login, name="login"),
    path("register/", views.register),
    path("add-emergency-contact/", views.add_emergency_contact, name="add_emergency_contact"),

    path("dashboard/", views.dashboard),
    path("alert/", views.emergency_page),
    path("contacts/", views.contacts_page),
    path("history/", views.history_page),
    path("map/", views.map_dashboard),
    path("save-alert/", views.save_alert),
    path("admin-dashboard/", views.admin_dashboard),
    path("user-dashboard/", views.user_dashboard),
    path("get-alerts/", views.get_alerts),
    path('create-user/', create_user),
]