from django.shortcuts import render, redirect, get_object_or_404

from accounts import models
from .models import Event
from .forms import EventForm
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from django.contrib import messages
from gallery.models import Gallery  # Import the Gallery model
from .utils import is_image_appropriate  # Import the utility function

@login_required
def event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data.get('image')
            
            # Validate image using NudeNet
            if image and not is_image_appropriate(image):
                messages.error(request, "Inappropriate content detected in the uploaded image. Please upload a different image.")
                galleries = Gallery.objects.all()  # Fetch all galleries
                return render(request, 'events/event_form.html', {'form': form,'galleries': galleries})

            # Proceed to save the event if the image is appropriate
            event = form.save(commit=False)
            event.creator = request.user  # Set the creator as the logged-in user
            event.save()
            messages.success(request, 'Event created successfully!')
            return redirect('event_list')
    else:
        form = EventForm()

    galleries = Gallery.objects.all()  # Fetch all galleries
    return render(request, 'events/event_form.html', {'form': form, 'galleries': galleries})
    
@login_required
def event_update(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            image = form.cleaned_data.get('image')
            
            # Validate image using NudeNet
            if image and not is_image_appropriate(image):
                messages.error(request, "Inappropriate content detected in the uploaded image.")
                return render(request, 'events/event_form.html', {'form': form})

            # Proceed to save the event if the image is appropriate
            form.save()
            messages.success(request, 'Event updated successfully!')
            return redirect('event_list')
    else:
        form = EventForm(instance=event)

    galleries = Gallery.objects.all()  # Fetch all galleries
    return render(request, 'events/event_form.html', {'form': form, 'galleries': galleries})  # Pass galleries to the template

@login_required
def event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        event.delete()
        messages.success(request, 'Event deleted successfully.')  # Add success message
        return redirect('event_list')
    return render(request, 'events/event_confirm_delete.html', {'event': event})

class EventListView(ListView):
    model = Event
    template_name = 'events/event_list.html'
    context_object_name = 'events'

class EventDetailView(DetailView):
    model = Event
    template_name = 'events/event_detail.html'
    context_object_name = 'event'
    
@login_required
def my_events_view(request):
    query = request.GET.get('q', '')
    events = Event.objects.all()

    if query:
        events = events.filter(
            models.Q(title__icontains=query) |
            models.Q(description__icontains=query) |
            models.Q(location__icontains=query) |
            models.Q(event_type__icontains=query)
        )

    return render(request, 'events/my_events.html', {'events': events, 'request': request})
