from django.db import models
from django.utils import timezone
from users.models import CustomUser
from faculty.models import Task, Deadline  # Importing Task & Deadline from faculty app

class StudentProgress(models.Model):
    """Stores student progress and proof of submission for completed tasks."""
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role': 'student'})
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    proof_of_submission = models.FileField(upload_to='submissions/', blank=True, null=True)  # Optional file upload
    submitted_at = models.DateTimeField(auto_now_add=True)
    reason_for_late_submission = models.TextField(blank=True, null=True)  # If student is late
    reviewed_by_faculty = models.BooleanField(default=False)  # Faculty review status
    progress_description = models.TextField(blank=True, null=True)
    delay_reason = models.TextField(blank=True, null=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    
    def is_late(self):
        """Check if the submission was late compared to the deadline."""
        deadline = Deadline.objects.filter(task=self.task, students=self.student).first()
        if deadline and self.submitted_at > deadline.due_date:
            return True
        return False

    def __str__(self):
        return f"Progress by {self.student.name} for {self.task.title}"
