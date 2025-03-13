from django.shortcuts import render, redirect
from .models import Task, Remark, Deadline  # Import the models
from .forms import TaskForm, RemarkForm, DeadlineForm  # Import the forms

def create_task(request):
    if request.user.is_authenticated and request.user.role == 'teacher':  # Check if the user is a faculty member
        if request.method == 'POST':
            form = TaskForm(request.POST)
            if form.is_valid():
                form.instance.faculty = request.user  # Automatically assign the logged-in faculty as the creator
                form.save()
                return redirect('faculty_dashboard')  # Redirect to dashboard after saving
        else:
            form = TaskForm()
        return render(request, 'faculty/create_task.html', {'form': form})
    else:
        return redirect('users:login')  # Redirect to login in users app

def faculty_dashboard(request):
    if request.user.is_authenticated and request.user.role == 'teacher':  # Check if the user is a faculty member
        tasks = Task.objects.filter(faculty=request.user)
        deadlines = Deadline.objects.filter(task__faculty=request.user)  # All deadlines for tasks assigned by the logged-in faculty
        remarks = Remark.objects.filter(task__faculty=request.user)
        return render(request, 'faculty/faculty_dashboard.html', {'tasks': tasks, 'deadlines': deadlines, 'remarks': remarks})
    else:
        return redirect('users:login')  # Redirect to login in users app


from .models import Deadline, Task
from users.models import CustomUser  # Assuming your user model is named `CustomUser`

def add_deadline(request):
    if request.method == 'POST':
        task_id = request.POST.get('task')
        student_id = request.POST.get('student')
        due_date = request.POST.get('due_date')

        try:
            task = Task.objects.get(id=task_id)
            student = CustomUser.objects.get(id=student_id)

            Deadline.objects.create(task=task, student=student, due_date=due_date)
            return redirect('faculty_dashboard')  # Redirect after successful submission

        except (Task.DoesNotExist, CustomUser.DoesNotExist):
            return render(request, 'faculty/faculty_dashboard.html', {
                'error': 'Invalid task or student selection.'
            })

    return redirect('faculty_dashboard')

def add_remark(request):
    if request.method == 'POST':
        task_id = request.POST.get('task')
        student_id = request.POST.get('student')
        remark_text = request.POST.get('remark')

        try:
            task = Task.objects.get(id=task_id)
            student = CustomUser.objects.get(id=student_id)

            Remark.objects.create(task=task, student=student, remark=remark_text)
            return redirect('faculty_dashboard')  # Redirect to the dashboard

        except (Task.DoesNotExist, CustomUser.DoesNotExist):
            return render(request, 'faculty/faculty_dashboard.html', {
                'error': 'Invalid task or student selection.'
            })

    return redirect('faculty_dashboard')
