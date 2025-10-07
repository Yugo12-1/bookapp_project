from django import forms
from .models import Book, BookUser
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'description', 'post_day']
        widgets = {
            'post_day': forms.DateInput(attrs={'type': 'date'})
        }

class SignupForm(UserCreationForm):
    class Meta:
        model = BookUser
        fields = ['username', 'password1', 'password2']

class LoginForm(AuthenticationForm):
    pass