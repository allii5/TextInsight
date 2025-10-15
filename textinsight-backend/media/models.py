from django.db import models
from authentication.models import User

class Media(models.Model):
    file_path = models.CharField(max_length=500)
    file_type = models.CharField(max_length=10, choices=[("image", "Image"), ("html", "HTML")])
    uploaded_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL) 
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Media uploaded by {self.uploaded_by.username}"
