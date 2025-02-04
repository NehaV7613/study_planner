from django.db import models  # type: ignore
from django.contrib.auth.models import AbstractUser, Group, Permission  # type: ignore


class AdminUser(AbstractUser):
    is_superadmin = models.BooleanField(default=True)

    # Add unique related_name to avoid conflicts
    groups = models.ManyToManyField(
        Group,
        related_name="adminuser_set",
        blank=True,
        help_text="The groups this admin belongs to.",
        verbose_name="groups",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="adminuser_permissions_set",
        blank=True,
        help_text="Specific permissions for this admin.",
        verbose_name="user permissions",
    )



from users.models import CustomUser  # Import the existing CustomUser model

class ApprovalRequest(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="approval_request")
    requested_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Approval Request - {self.user.username} ({self.user.role})"




class Syllabus(models.Model):
    title = models.CharField(max_length=255)
    course_code = models.CharField(max_length=20, unique=True)  # Unique identifier for each course
    uploaded_at = models.DateTimeField(auto_now_add=True)
    syllabus_file = models.FileField(upload_to="syllabus/")  # File upload field

    def __str__(self):
        return f"{self.title} ({self.course_code})"
