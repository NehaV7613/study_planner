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
    path("to_do/", views.student_tasks, name="student_tasks"),
    path("to_do/add/", views.student_add_task, name="student_add_task"),
    path("to_do/toggle/<int:task_id>/", views.student_toggle_task, name="student_toggle_task"),
    path("to_do/delete/<int:task_id>/", views.student_delete_task, name="student_delete_task"),
]