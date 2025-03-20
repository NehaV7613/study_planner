from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, get_backends
from django.contrib import messages
from users.models import CustomUser  # Import your CustomUser model
from django.contrib.auth.decorators import login_required
from faculty.models import Deadline, Remark, Task
from .models import StudentProgress
from .forms import StudentProgressForm


@login_required
def student_dashboard(request):
    """Display student progress, deadlines, and faculty remarks on the dashboard."""
    
    if request.user.role != 'student':
        return redirect("student_login")  # Prevent non-students from accessing

    student = request.user  # Logged-in student
    
    # Fetch upcoming deadlines
    deadlines = Deadline.objects.filter(students=student).select_related('task').order_by('due_date')
    
    # Fetch faculty remarks
    remarks = Remark.objects.filter(student=student).select_related('task').order_by('-created_at')
    
    # Fetch student progress
    student_progress = StudentProgress.objects.filter(student=student)

    # Pass all data to the template
    context = {
        'deadlines': deadlines,
        'remarks': remarks,
        'student_progress': student_progress,  # Ensure progress is passed!
    }

    return render(request, 'student/student_dashboard.html', context)


def pomodoro(request):
    return render(request, 'student/pomodoro.html')

def student_login(request):
    if request.method == "POST":
        student_id = request.POST.get("student_id", "").strip()
        password = request.POST.get("password", "").strip()

        print(f"Received student_id: {student_id}")  # Debugging

        # Fetch user by student_id
        user = CustomUser.objects.filter(student_id=student_id).first()

        if user:
            print(f"User found: {user.username}, Stored role: {user.role}")  # Debugging

            password_valid = user.check_password(password)
            print(f"Password match: {password_valid}")  # Debugging

            if password_valid and user.role == "student":
                # Identify the backend dynamically
                backend = get_backends()[0]  # Select the first backend (update if needed)
                user.backend = f"{backend.__module__}.{backend.__class__.__name__}"  # Set backend explicitly

                login(request, user)  # Now login should work
                print("Login successful!")  # Debugging
                return redirect("student_dashboard")

        messages.error(request, "Invalid student credentials!")
        print("Login failed!")  # Debugging

    return render(request, "student/student_login.html")

from django.contrib.auth import logout


def student_logout(request):
    logout(request)  # Logs out the current user
    return redirect("student_login")  # Redirect to login page


@login_required
def submit_progress(request):
    """Handles student progress submission and displays progress history."""
    if request.user.role != 'student':
        return redirect('student_login')  # Prevent non-students from submitting

    if request.method == "POST":
        form = StudentProgressForm(request.POST, request.FILES)
        if form.is_valid():
            progress = form.save(commit=False)
            progress.student = request.user
            progress.save()
            return redirect('student_dashboard')  # Redirect after submission
    else:
        form = StudentProgressForm()

    # ✅ Fetch progress data for the logged-in student
    student_progress = StudentProgress.objects.filter(student=request.user)

    return render(request, 'student/submit_progress.html', {
        'form': form,
        'student_progress': student_progress,  # Pass progress records to template
    })


@login_required
def faculty_review_progress(request):
    """Allows faculty to review student progress submissions."""
    if request.user.role != 'teacher':
        return redirect('student_dashboard')  # Only faculty can access this page

    student_submissions = StudentProgress.objects.all()

    return render(request, 'faculty/review_progress.html', {'student_submissions': student_submissions})