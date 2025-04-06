from django.urls import path
from . import views

urlpatterns = [
    path("faculty_dashboard/", views.faculty_dashboard, name="faculty_dashboard"),
    path("add_task/", views.add_task, name="add_task"),
    path("add_deadline/", views.add_deadline, name="add_deadline"),
    path("add_remark/", views.add_remark, name="add_remark"),
    path("login/", views.faculty_login, name="faculty_login"),
    path("logout/", views.faculty_logout, name="faculty_logout"),
    path("faculty/review/<int:progress_id>/", views.review_submission_page, name="review_submission_page"),
    path("faculty/review/mark/<int:progress_id>/", views.mark_submission_reviewed, name="mark_submission_reviewed"),
]