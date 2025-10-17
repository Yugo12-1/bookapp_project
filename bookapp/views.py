from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Book, Review
from .form import BookForm, SignupForm, LoginForm, ReviewForm

# Create your views here.

"""
This section is for base funcitons of book app.
There are functions with CRUD capbilities.
All functions are login required.

CREATE (create_func())
 Crate a new post.

READ (list_func(), detail_func())
 See a list and details of posts.

UPDATE (edit_func())
 Edit a post.

DELETE (delete_func())
 Delete a post.
"""

@login_required
def list_func(request):
    books = Book.objects.all()
    # Add total reputation
    books_reputation = cal_avg_reputation(books)
    return render(request, 'book/list.html', {
        'books': books,
        'books_reputation': books_reputation,
    })

@login_required
def detail_func(request, pk):
    book = get_object_or_404(Book, pk=pk)
    # reviews(related_name) 
    reviews = book.reviews.all()
    return render(request, 'book/detail.html', {
        'book':book,
        'reviews': reviews
    })

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

signup_func()
 Sign up bookapp user.

login_func()
 Log in for bookapp user. It makes users user bookapp basic functions.

logout_func()
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
This section is for Review funciton
Book_user and any other user can post a review for a book

review_create()
 Create a review post for book.

review_edit()
 Edit your review post.

review_delete()
 Delete your review post.
"""

@login_required
def review_create(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            # Django automaticaly bind ForeignKey and object
            review.book = book
            review.review_user = request.user
            review.save()
            return redirect('detail', pk=book_id)
    else:
        form = ReviewForm()
        return render(request, 'review/review_create.html', {'form':form})

@login_required
def review_edit(request, book_id, pk):
    review = get_object_or_404(Review, pk=pk)

    # check user ojbect
    if review.review_user != request.user:
        return HttpResponseForbidden("あなたはこのレビューを編集できません。")
    
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            review_form = form.save(commit=False)
            review_form.review_user = review.review_user
            review_form.book = review.book
            review_form.save()
            return redirect('detail', pk=book_id)
    else:
        form = ReviewForm(instance=review)
        return render(request, 'review/review_edit.html', {'form':form})

@login_required
def review_delete(request, book_id, pk):
    review = get_object_or_404(Review, pk=pk)

    # check user ojbect
    if review.review_user != request.user:
        return HttpResponseForbidden("あなたはこのレビューを削除できません。")

    if request.method == 'POST':
        review.delete()
        return redirect('detail', pk=book_id)
    else:
        return render(request, 'review/review_delete.html', {'book_id':book_id})

"""
Any other function
"""

def cal_avg_reputation(books):
    books_reputation = {}
    
    for book in books:
        # reviews querryset
        reviews = book.reviews.all()
        if reviews.exists():
            total_reputation = 0
            total_count = reviews.count()
            for review in reviews:
                total_reputation += review.reputation            
            book_avg_reputation = round(total_reputation/total_count, 1)
            books_reputation[book.id] = book_avg_reputation
        else:
            book_avg_reputation = 0
        
        books_reputation[book.id] = book_avg_reputation

    return books_reputation