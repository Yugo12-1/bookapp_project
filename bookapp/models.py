from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Create your models here.

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=50)
    description = models.TextField()
    post_day = models.DateField(auto_now=False, auto_now_add=False)
    book_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='books'
    )

    def __str__(self):
        return self.title

class BookUser(AbstractUser):
    pass

class Reveiw(models.Model):
    content = models.TextField()
    create_day = models.DateField(auto_now=False, auto_now_add=False)
    reputation = models.IntegerField()
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    book_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reviews'
    )

    def __str__(self):
        return f"{self.book.title} - {self.book_user.username}"