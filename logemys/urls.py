"""Define URL patterns for logemys"""

from django.urls import path
from . import views

app_name = 'logemys'
urlpatterns = [
    # Home Page
    path('', views.index, name='index'),
    # Topics page
    path('topics/', views.topics, name='topics'),
    # One Topic
    path('topics/<int:topic_id>/', views.topic, name='topic')
]