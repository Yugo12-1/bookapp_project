from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Book
from .form import BookForm, SignupForm, LoginForm

# Create your views here.

"""
This section is for base funcitons of book app.
There are functions with CRUD capbilities.

CREATE (create_func)
 crate a new post.

READ (list_func, detail_func)
 see a list and details of posts

UPDATE (edit_func)
 edit a post

DELETE (delete_func)
 delete a post
"""

@login_required
def list_func(request):
    books = Book.objects.all()
    return render(request, 'book/list.html', {'books': books})

@login_required
def detail_func(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'book/detail.html', {'book':book})

@login_required
def create_func(request):
    # create a post
    if request.method == 'POST':
        # use forms.ModelForm
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list')
        # Invalid input is checked with form.py
    else:
        # create blank form (GET method)
        form = BookForm()
        return render(request, 'book/create.html', {'form':form})


def delete_func(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('list')
    return render(request, 'book/delete.html', {'book':book})


def edit_func(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        # use existing form
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('detail', pk=pk)
    else:
        form = BookForm(instance=book)
        return render(request, 'book/edit.html', {'form':form, 'book':book})

"""
This section is for login functions for book app

signup_func(), login_func(), logout_func()

"""

def signup_func(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list')
        else:
            return render(request, 'book/signup.html', {'form':form})
    else:
        # create a black form
        form = SignupForm()
        return render(request, 'book/signup.html', {'form':form})


def login_func(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('list')
        else:
            error = 'ユーザー名もしくはパスワードが間違っています'
            return render(request, 'book/login.html', {'form': form, 'error':error})
    else:
        form = LoginForm()
        return render(request, 'book/login.html', {'form':form})


def logout_func(request):
    logout(request)
    return redirect('login')