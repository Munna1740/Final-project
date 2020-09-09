from django.db import models

class Questions(models.Model):
    category = models.CharField(max_length=150, null=True)
    question = models.CharField(max_length=200, null=True)
    answer = models.CharField(max_length=400, null=True)
    tag = models.CharField(max_length=150, null=True)
