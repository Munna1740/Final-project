from django.db import models
from django.contrib.auth.models import User


# Create your models

class UserInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    key_skills = models.CharField(max_length=200, null=True)
    job_area = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.user.username

class UserResume(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    resume = models.FileField()
    upload_date = models.DateTimeField(auto_now_add=True)


