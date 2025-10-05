from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'description', 'post_day']
        widgets = {
            'post_day': forms.DateInput(attrs={'type': 'date'})
        }
