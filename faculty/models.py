from django.db import models
from users.models import CustomUser
 # Assuming User model is in the users app

class Task(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    faculty = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="faculty_tasks")
    
    def __str__(self):
        return self.name

class Deadline(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="student_deadlines")
    due_date = models.DateTimeField()
    status = models.CharField(max_length=50, choices=[('Pending', 'Pending'), ('Completed', 'Completed')])
    
    def __str__(self):
        return f"{self.task.name} - {self.student.username}"

class Remark(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="student_remarks")
    remark = models.TextField()
    
    def __str__(self):
        return f"Remark for {self.student.username} on {self.task.name}"


