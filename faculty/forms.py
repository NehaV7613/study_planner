from django import forms
from .models import Task, Deadline, Remark
from users.models import CustomUser 
from student.models import StudentProgress 

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description']

class DeadlineForm(forms.ModelForm):
    task = forms.ModelChoiceField(
        queryset=Task.objects.all(),
        empty_label="Select a task",
        widget=forms.Select(attrs={'class': 'form-control'})  
    )

    students = forms.ModelMultipleChoiceField(
        queryset=CustomUser.objects.filter(role='student'),
        widget=forms.CheckboxSelectMultiple,  # Allows selecting multiple students
        label="Students"
    )

    class Meta:
        model = Deadline
        fields = ['task', 'students', 'due_date']

class RemarkForm(forms.ModelForm):
    task = forms.ModelChoiceField(
        queryset=Task.objects.all(),
        empty_label="Select a task",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    student = forms.ModelChoiceField(
        queryset=CustomUser.objects.filter(role='student'),
        empty_label="Select a student",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Remark
        fields = ['task', 'student', 'remark']
        

from student.models import StudentProgress

class FacultyReviewForm(forms.ModelForm):
    class Meta:
        model = StudentProgress
        fields = ['reviewed_by_faculty', 'reviewed_at']