from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils.timezone import now, make_aware
from datetime import datetime
from django.contrib.auth import login, logout
from .models import Task, Deadline, Remark
from users.models import CustomUser
from student.models import StudentProgress
from django.contrib.auth.decorators import login_required


@login_required
def faculty_dashboard(request):
    """Faculty dashboard displaying tasks, deadlines, and remarks"""

    if request.user.role != 'teacher':
        return redirect("faculty_login")

    tasks = Task.objects.filter(faculty=request.user)

    # Get upcoming deadlines
    deadlines = Deadline.objects.filter(
        task__faculty=request.user, due_date__gte=now()
    ).prefetch_related('students')

    remarks = Remark.objects.filter(faculty=request.user).select_related('student')

    students = CustomUser.objects.filter(role='student')

    # ✅ Get all unreviewed student progress submissions
    pending_reviews = StudentProgress.objects.filter(
        task__faculty=request.user, reviewed_by_faculty=False
    ).select_related('student', 'task')

    # ✅ Get all reviewed submissions
    reviewed_submissions = StudentProgress.objects.filter(
        task__faculty=request.user, reviewed_by_faculty=True
    ).select_related('student', 'task')

    return render(request, 'faculty/faculty_dashboard.html', {
        'tasks': tasks,
        'deadlines': deadlines,
        'remarks': remarks,
        'students': students,
        'pending_reviews': pending_reviews,
        'reviewed_submissions': reviewed_submissions  # ✅ Pass reviewed submissions
    })


def add_task(request):
    """Faculty adds a task manually"""
    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        description = request.POST.get("description", "").strip()

        if not title:
            messages.error(request, "Task title cannot be empty!")
            return redirect("faculty_dashboard")

        Task.objects.create(faculty=request.user, title=title, description=description)
        messages.success(request, "Task added successfully!")

    return redirect("faculty_dashboard")

def add_deadline(request):
    """Faculty assigns a deadline to a task for multiple students"""
    if request.method == "POST":
        task_id = request.POST.get("task")
        student_ids = request.POST.getlist("students")
        due_date_str = request.POST.get("due_date")

        try:
            due_date = make_aware(datetime.strptime(due_date_str, "%Y-%m-%dT%H:%M"))
        except ValueError:
            messages.error(request, "Invalid date format!")
            return redirect("faculty_dashboard")

        task = get_object_or_404(Task, id=task_id, faculty=request.user)
        students = CustomUser.objects.filter(id__in=student_ids, role="student")

        if not students.exists():
            messages.error(request, "No valid students selected!")
            return redirect("faculty_dashboard")

        deadline = Deadline.objects.create(task=task, due_date=due_date)
        deadline.students.set(students)
        messages.success(request, "Deadline added successfully!")

    return redirect("faculty_dashboard")

def add_remark(request):
    """Faculty adds a remark for an **individual** student"""
    if request.method == "POST":
        task_id = request.POST.get("task")
        student_id = request.POST.get("student")
        remark_text = request.POST.get("remark", "").strip()

        if not remark_text:
            messages.error(request, "Remark cannot be empty!")
            return redirect("faculty_dashboard")

        task = get_object_or_404(Task, id=task_id, faculty=request.user)
        student = get_object_or_404(CustomUser, id=student_id, role="student")

        remark = Remark.objects.create(task=task, faculty=request.user, student=student, remark=remark_text)
        messages.success(request, f"Remark added for {student.name}!")

    return redirect("faculty_dashboard")

def faculty_login(request):
    """Handles faculty login"""
    if request.method == "POST":
        faculty_id = request.POST.get("faculty_id")
        password = request.POST.get("password")

        user = CustomUser.objects.filter(faculty_id=faculty_id, role="teacher").first()

        if user and user.check_password(password):
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect("faculty_dashboard")

        messages.error(request, "Invalid faculty credentials!")
    
    return render(request, "faculty/faculty_login.html")


def faculty_logout(request):
    """Logs out faculty members"""
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect("faculty_login")


def upcoming_deadlines(request):
    """Fetch upcoming tasks that have a due date in the future"""
    tasks = Task.objects.filter(due_date__gte=now()).order_by("due_date")  # Adjust if due_date exists

    return render(request, "faculty/upcoming_deadlines.html", {"tasks": tasks})

@login_required
def review_submission_page(request, progress_id):
    """Faculty reviews a student's submission before marking it as reviewed."""

    if not progress_id:
        messages.error(request, "Invalid submission ID.")
        return redirect("faculty_dashboard")

    submission = get_object_or_404(StudentProgress, id=progress_id)

    if request.user.role != 'teacher':
        messages.error(request, "You are not authorized to review submissions.")
        return redirect("faculty_dashboard")  

    return render(request, "faculty/review_submission.html", {"submission": submission})


@login_required
def mark_submission_reviewed(request, progress_id):
    """Mark a student submission as reviewed"""

    if not progress_id:
        messages.error(request, "Invalid submission ID.")
        return redirect("faculty_dashboard")

    submission = get_object_or_404(StudentProgress, id=progress_id)

    if request.user.role != 'teacher':
        messages.error(request, "You are not authorized to review submissions.")
        return redirect("faculty_dashboard")  

    # Mark as reviewed
    submission.reviewed_by_faculty = True
    submission.reviewed_at = now()  # Store review timestamp
    submission.save()

    messages.success(request, "Submission reviewed successfully!")
    return redirect("faculty_dashboard")  