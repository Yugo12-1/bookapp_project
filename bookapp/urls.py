from django.contrib import admin
from django.urls import path, include
from .views import list_func, detail_func, create_func, delete_func, edit_func
from .views import signup_func, login_func, logout_func
from .views import review_create, review_edit, review_delete

urlpatterns = [
    path('book/list/', list_func, name='list'),
    path('book/<int:pk>', detail_func, name='detail'),
    path('book/create/', create_func, name='create'),
    path('book/<int:pk>/delete/', delete_func, name='delete'),
    path('book/<int:pk>/edit/', edit_func, name='edit'),
    path('account/signup/', signup_func, name='signup'),
    path('account/login/', login_func, name='login'),
    path('account/logout/', logout_func, name='logout'),
    path('book/review/create/<int:book_id>', review_create, name='review_create'),
    path('book/review/edit/<int:book_id>/<int:pk>', review_edit, name='review_edit'),
    path('book/review/delete/<int:book_id>/<int:pk>', review_delete, name='review_delete'),
]