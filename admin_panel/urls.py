from django.urls import path
from django.contrib.auth import views as auth_views
from .views import approve_users
from . import views

urlpatterns = [
    path('register/', views.register_admin, name='admin_register'),
    path('login/', views.admin_login, name='admin_login'), 
    path('dashboard/', views.dashboard, name='admin_dashboard'),  # Add later for dashboard
    path('approve_users/', approve_users, name='approve_users'),

]
