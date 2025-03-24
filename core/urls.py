from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='index'),
     path("ai-lesson-planner/", views.ai_lesson_planner, name="ai_lesson_planner"),
    
]
