from django.contrib.auth.forms import UserCreationForm
from .models import AdminUser

class AdminUserCreationForm(UserCreationForm):
    class Meta:
        model = AdminUser
        fields = ['username', 'email', 'password1', 'password2']  # Add other fields as necessary
