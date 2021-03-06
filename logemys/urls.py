"""Define URL patterns for logemy"""

from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

app_name = 'logemys'
urlpatterns = [
    # Home Page
    path('', views.base, name='base'),

    path('', views.index, name='index'),
    # Topics page
    path('topics/', views.topics, name='topics'),
    # One Topic
    path('topics/<int:topic_id>/', views.topic, name='topic'),
    # New Topic
    path('new_topic/', views.new_topic, name='new_topic'),
    # New Entry
    path('new_entry/<int:topic_id>/', views.new_entry, name='new_entry'),
    # Edit Entry
    path('edit_entry/<int:entry_id>/', views.edit_entry, name='edit_entry'),
]
urlpatterns += staticfiles_urlpatterns()
