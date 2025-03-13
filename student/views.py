from django.shortcuts import render

# Create your views here.
def student_dashboard(request):
    return render(request, 'student/student_dashboard.html')

def pomodoro(request):
    return render(request, 'student/pomodoro.html')