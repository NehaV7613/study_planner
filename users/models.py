from django.contrib.auth.models import AbstractUser, Group, Permission  # type: ignore
from django.db import models  # type: ignore


class CustomUser(AbstractUser):
    STUDENT = 'student'
    TEACHER = 'teacher'
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    ]
    name = models.CharField(max_length=150, blank=False)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
    student_id = models.CharField(max_length=15, blank=True, null=True)
    faculty_id = models.CharField(max_length=15, blank=True, null=True)
    is_superadmin = models.BooleanField(default=False) 

    # Add unique related_name to avoid conflicts
    groups = models.ManyToManyField(
        Group,
        related_name="customuser_set",
        blank=True,
        help_text="The groups this user belongs to.",
        verbose_name="groups",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="customuser_permissions_set",
        blank=True,
        help_text="Specific permissions for this user.",
        verbose_name="user permissions",
    )

    def save(self, *args, **kwargs):
        # Ensure only one ID is populated based on the role
        if self.role == 'student':
            self.faculty_id = None
        elif self.role == 'teacher':
            self.student_id = None
        super().save(*args, **kwargs)
        
        
