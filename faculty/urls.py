from django.urls import path
from . import views

urlpatterns = [
    path('faculty_dashboard/', views.faculty_dashboard, name='faculty_dashboard'),
    path('add_deadline/', views.add_deadline, name='add_deadline'),
    path('add_remark/', views.add_remark, name='add_remark'),
]
