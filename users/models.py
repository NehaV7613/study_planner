from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    ]
    name = models.CharField(max_length=150, blank=False)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
    student_id = models.CharField(max_length=15, blank=True, null=True)
    faculty_id = models.CharField(max_length=15, blank=True, null=True)

    def save(self, *args, **kwargs):
        # Ensure only one ID is populated based on the role
        if self.role == 'student':
            self.faculty_id = None
        elif self.role == 'teacher':
            self.student_id = None
        super().save(*args, **kwargs)
