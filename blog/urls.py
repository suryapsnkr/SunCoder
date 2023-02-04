from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.blogHome, name="blogHome"),
    path('blog/addPost', views.addPost, name="addPost"),
    path('blog/postComment', views.postComment, name="postComment"),
    path('<str:slug>', views.blogPost, name="blogPost"),
    
]
