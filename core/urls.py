from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('ai-lesson-planner/', views.ai_lesson_planner, name='ai_lesson_planner'),
    path('ai-study-planner/', views.ai_study_planner, name='ai_study_planner'),
]