from django.shortcuts import render, redirect, get_object_or_404
from .models import Topic, Entry
from .forms import TopicForm, EntryForm
from django.contrib.auth.decorators import login_required
from django.http import Http404


# Create your views here.
def index(request):
    """The home page for Learning Log."""
    return render(request, 'logemys/index.html')


def base(request):
    """The Home poge for Logemys"""
    return render(request, 'logemys/templates/logemys/base.html')


def check_owner(topic, request):
    if topic.owner != request.user:
        raise Http404


@login_required
def topics(request):
    """Show all topics"""
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics}
    return render(request, 'logemys/topics.html', context)


@login_required
def topic(request, topic_id):
    """One Topic"""
    topic = get_object_or_404(Topic, id=topic_id)
    # Make sure the topic belongs to the current user
    check_owner(topic, request)
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'logemys/topic.html', context)


@login_required
def new_topic(request):
    """Add new topic"""
    check_owner(topic, request)
    if request.method != 'POST':
        # No data submitted, create a blank form
        form = TopicForm()
    else:
        # POST , Process form
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return redirect('logemys:topics')

    # Display a blank or invalid form
    context = {'form': form}
    return render(request, 'logemys/new_topic.html', context)


@login_required
def new_entry(request, topic_id):
    """Add a new entry for a particular topic"""
    topic = Topic.objects.get(id=topic_id)
    check_owner(topic, request)
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


@login_required
def edit_entry(request, entry_id):
    """Editing an existing entry"""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    check_owner(topic, request)
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
