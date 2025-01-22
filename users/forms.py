from django import forms # type: ignore
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm # type: ignore
from .models import CustomUser

# Custom user creation form
class CustomUserCreationForm(UserCreationForm):
    name = forms.CharField(max_length=150, required=True)
    role = forms.ChoiceField(choices=CustomUser.ROLE_CHOICES, required=True)
    student_id = forms.CharField(max_length=15, required=False)
    faculty_id = forms.CharField(max_length=15, required=False)

    class Meta:
        model = CustomUser
        fields = ['name', 'username', 'email', 'password1', 'password2', 'role', 'student_id', 'faculty_id']
        labels = {
            'name': 'Name',
            'username': 'Username',
            'email': 'Email',
            'password1': 'Password',
            'password2': 'Confirm Password',
            'role': 'Role',
            'student_id': 'Student ID',
            'faculty_id': 'Faculty ID',
        }

    def clean(self):
        cleaned_data = super().clean()
        role = cleaned_data.get("role")
        student_id = cleaned_data.get("student_id")
        faculty_id = cleaned_data.get("faculty_id")

        # Validation logic for role-specific fields
        if role == "student":
            if not student_id:
                self.add_error("student_id", "Student ID is required for students.")
            if faculty_id:
                self.add_error("faculty_id", "Faculty ID should not be filled for students.")
        elif role == "teacher":
            if not faculty_id:
                self.add_error("faculty_id", "Faculty ID is required for teachers.")
            if student_id:
                self.add_error("student_id", "Student ID should not be filled for teachers.")

        return cleaned_data
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
        if field.label:  # Ensure label is not None
            field.label = field.label.capitalize()
        self.fields['role'].widget.attrs['class'] = 'form-select'




# Custom authentication form to handle login errors

class CustomAuthenticationForm(AuthenticationForm):
    def clean(self):
        cleaned_data = super().clean()

        # Remove duplicate error message
        if '__all__' in self.errors:
            del self.errors['__all__']
        
        return cleaned_data
    
