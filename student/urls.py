from django.urls import path
from . import views

urlpatterns = [
    #path('', views.index, name='index'),
    path('student_dashboard/', views.student_dashboard, name='student_dashboard'),
    path('pomodoro/', views.pomodoro, name='pomodoro'), 
    path('login/', views.student_login, name="student_login"),
    path("logout/", views.student_logout, name="student_logout"),
    path('submit-progress/', views.submit_progress, name='submit_progress'),
    path('faculty-review/', views.faculty_review_progress, name='faculty_review_progress'),
]