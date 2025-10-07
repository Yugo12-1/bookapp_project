from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=50)
    description = models.TextField()
    post_day = models.DateField(auto_now=False, auto_now_add=False)

    def __str__(self):
        return self.title

class BookUser(AbstractUser):
    pass