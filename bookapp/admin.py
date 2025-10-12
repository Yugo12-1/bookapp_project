from django.contrib import admin
from .models import Book, BookUser, Reveiw

# Register your models here.
admin.site.register(Book)
admin.site.register(BookUser)
admin.site.register(Reveiw)