from django.urls import path
from . import views

urlpatterns = [

    path("", views.user_login),   # default page

    path("login/", views.user_login, name="login"),
    path("register/", views.register),

    path("dashboard/", views.dashboard),
    path("alert/", views.emergency_page),
    path("contacts/", views.contacts_page),
    path("history/", views.history_page),
    path("map/", views.map_dashboard),
    path("save-alert/", views.save_alert),
    path("admin-dashboard/", views.admin_dashboard),
    path("user-dashboard/", views.user_dashboard),
    path("get-alerts/", views.get_alerts),
]