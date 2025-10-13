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

class Review(models.Model):
    RATING_CHOICES = {
        1: '★☆☆☆☆',
        2: '★★☆☆☆',
        3: '★★★☆☆',
        4: '★★★★☆',
        5: '★★★★★'
    }
    
    content = models.TextField()
    create_day = models.DateField(auto_now=False, auto_now_add=False)
    reputation = models.IntegerField(choices=RATING_CHOICES)
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    review_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reviews'
    )

    def __str__(self):
        return f"{self.book.title} - {self.review_user.username}"