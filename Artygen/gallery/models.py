# gallery/models.py
from django.db import models
from django.contrib.auth.models import User

class Gallery(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)  # Owner will be a user
    location = models.CharField(max_length=255)
    theme = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name
