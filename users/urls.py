"""Defines URL pattern for users"""
from django.urls import path, include
from . import views
app_name = 'users'
urlpatterns = [
    # include default auth urls
    path('', include('django.contrib.auth.urls')),
    # Registration page
    path('register/', views.register, name='register'),
]