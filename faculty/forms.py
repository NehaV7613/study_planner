from django import forms
from .models import Task, Deadline, Remark

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description']

class DeadlineForm(forms.ModelForm):
    class Meta:
        model = Deadline
        fields = ['task', 'student', 'due_date', 'status']

class RemarkForm(forms.ModelForm):
    class Meta:
        model = Remark
        fields = ['task', 'student', 'remark']
