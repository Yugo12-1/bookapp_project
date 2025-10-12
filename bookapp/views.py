from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Book
from .form import BookForm, SignupForm, LoginForm

# Create your views here.

"""
This section is for base funcitons of book app.
There are functions with CRUD capbilities.
All functions are login required.

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
        # Invalid input is checked with form.py
        if form.is_valid():
            # get an object not in DB
            book = form.save(commit=False)
            # set book_user filed
            book.book_user = request.user
            book.save()
            return redirect('list')
    else:
        # create blank form (GET method)
        form = BookForm()
        return render(request, 'book/create.html', {'form':form})

@login_required
def delete_func(request, pk):
    book = get_object_or_404(Book, pk=pk)
    # delete by only crete user
    if book.book_user != request.user:
        return HttpResponseForbidden("あなたはこの本を削除できません。")
    if request.method == 'POST':
        book.delete()
        return redirect('list')
    # when method is GET
    else:
        return render(request, 'book/delete.html', {'book':book})

@login_required
def edit_func(request, pk):
    book = get_object_or_404(Book, pk=pk)
    # edit by only crete user
    if book.book_user != request.user:
        return HttpResponseForbidden("あなたはこの本を編集できません。")
    if request.method == 'POST':
        # use existing form
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('detail', pk=pk)
    # when method is GET
    else:
        form = BookForm(instance=book)
        return render(request, 'book/edit.html', {'form':form, 'book':book})

"""
This section is for login functions for book app.
SignupForm and LoginForm are used from form.py.

signup_func
 Sign up bookapp user.

login_func
 Log in for bookapp user. It makes users user bookapp basic functions.

logout_func
 Log out for bookapp user. 
"""

def signup_func(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list')
        else:
            return render(request, 'account/signup.html', {'form':form})
    else:
        # create a black form
        form = SignupForm()
        return render(request, 'account/signup.html', {'form':form})

def login_func(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('list')
        else:
            error_for_login = 'ユーザー名もしくはパスワードが間違っています'
            return render(request, 'account/login.html', {'form': form, 'error_for_login':error_for_login})
    else:
        form = LoginForm()
        return render(request, 'account/login.html', {'form':form})

def logout_func(request):
    logout(request)
    return redirect('login')

"""

"""