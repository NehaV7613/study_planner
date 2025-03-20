from django.db import models
from django.utils import timezone 
from users.models import CustomUser

class Task(models.Model):
    """Stores tasks manually added by faculty."""
    faculty = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role': 'teacher'})
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return self.title

class Deadline(models.Model):
    """Stores deadlines for tasks assigned to students."""
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    due_date = models.DateTimeField()
    students = models.ManyToManyField(CustomUser, limit_choices_to={'role': 'student'})
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.task.title} - {self.due_date}"

class Remark(models.Model):
    """Faculty can add remarks for an **individual** student."""
    faculty = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="faculty_remarks"
    )
    student = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="student_remarks", 
        limit_choices_to={'role': 'student'}, null=True, blank=True  # Allow NULL temporarily
    )
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    remark = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Remark by {self.faculty.name} for {self.student.name} on {self.task.title}"


