from django.db import models
from authentication.models import User
from classes.models import Class

class Assignment(models.Model):
    title = models.CharField(max_length=255, blank=False)
    description = models.TextField(blank=False)
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='assignments')  
    expected_keywords = models.JSONField() 
    due_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Essay(models.Model):
    title = models.CharField(max_length=255, blank=False)
    content = models.TextField(blank=False)
    submission_date = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[("pending", "Pending"), ("reviewed", "Reviewed"), ("resubmitted", "Resubmitted")], default="pending")
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='essays') 
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='essays')  
    submission_count = models.IntegerField(default=1)

    def __str__(self):
        return self.title



