from django.db import models
from authentication.models import User

class Class(models.Model):
    class_name = models.CharField(max_length=255, blank=False)
    class_code = models.CharField(max_length=50, unique=True)
    teacher_name = models.CharField(max_length=255)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='classes')  # Relating to the teacher
    student_limit = models.IntegerField(default=50)
    student_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.class_name

class ClassStudents(models.Model):
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='students')  # ForeignKey to Class
    student_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='student_classes')  # ForeignKey to User (Student)
    enrollment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student_id.username} in {self.class_id.class_name}"
