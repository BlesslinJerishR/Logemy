from django.shortcuts import render, redirect
from .models import Topic, Entry
from .forms import TopicForm, EntryForm


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


def new_topic(request):
    """Add new topic"""
    if request.method != 'POST':
        # No data submitted, create a blank form
        form = TopicForm()
    else:
        # POST , Process form
        form = TopicForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('logemys:topics')

    # Display a blank or invalid form
    context = {'form': form}
    return render(request, 'logemys/new_topic.html', context)


def new_entry(request, topic_id):
    """Add a new entry for a particular topic"""
    topic = Topic.objects.get(id=topic_id)

    if request.method != 'POST':
        # No data submitted, create a blank form
        form = EntryForm()
    else:
        # POST data submitted, Process Data.
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return redirect('logemys:topic', topic_id=topic_id)
    # Display a blank or invalid form
    context = {'topic': topic, 'form': form}
    return render(request, 'logemys/new_entry.html', context)


def edit_entry(request, entry_id):
    """Editing an existing entry"""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic

    if request.method != 'POST':
        # Initial request; Pre fill the form with the current entry
        form = EntryForm(instance=entry)
    else:
        # POST data submitted; Process data.
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('logemys:topic', topic_id=topic.id)

    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'logemys/edit_entry.html', context)
