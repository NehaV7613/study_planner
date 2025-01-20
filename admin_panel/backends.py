from django.contrib.auth.backends import BaseBackend
from users.models import CustomUser

class AdminAuthBackend(BaseBackend):
    """
    Custom authentication backend for admins.
    Only allows users with `is_superadmin=True` to log in via this backend.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # Fetch user where `is_superadmin=True` (case-insensitive username lookup)
            user = CustomUser.objects.get(username__iexact=username, is_superadmin=True)
            
            # Check if the user is active and password matches
            if user.is_active and user.check_password(password):
                return user
        except CustomUser.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return CustomUser.objects.get(pk=user_id, is_superadmin=True)
        except CustomUser.DoesNotExist:
            return None
