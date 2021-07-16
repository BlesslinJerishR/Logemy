from django.shortcuts import render
from .models import Topic


# Create your views here.
def index(request):
    """The Home poge for Logemys"""
    return render(request, 'logemys/home.html')


def topics(request):
    """Show all topics"""
    topics = Topic.objects.order_by('date_added')
    context = {'topics': topics}
    return render(request, 'logemys/topics.html', context)


def topic(request, topic_id):
    """One Topic"""
    topic = Topic.objects.get(id=topic_id)
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'logemys/topic.html', context)
