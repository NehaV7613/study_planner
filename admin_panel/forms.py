from django.contrib.auth.forms import UserCreationForm
from .models import AdminUser

class AdminUserCreationForm(UserCreationForm):
    class Meta:
        model = AdminUser
        fields = ['username', 'email', 'password1', 'password2']  # Add other fields as necessary

from django import forms
from .models import Syllabus

class SyllabusUploadForm(forms.ModelForm):
    class Meta:
        model = Syllabus
        fields = ['title', 'course_code', 'syllabus_file']
