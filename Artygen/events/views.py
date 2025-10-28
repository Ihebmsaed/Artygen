from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from accounts import models
from .models import Event
from .forms import EventForm
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from django.contrib import messages
from gallery.models import Gallery  # Import the Gallery model
from .utils import is_image_appropriate  # Import the utility function
from .event_description_generator import get_event_description_generator

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
def generate_event_description(request):
    """
    Vue pour générer une description d'événement avec IA via AJAX
    """
    if request.method == 'POST':
        title = request.POST.get('title', '')
        event_type = request.POST.get('event_type', '')
        location = request.POST.get('location', '')
        date = request.POST.get('date', '')
        capacity = request.POST.get('capacity', '')
        tone = request.POST.get('tone', 'professional')

        # Validation basique
        if not title or not event_type:
            return JsonResponse({'success': False, 'error': 'Titre et type d\'événement requis'})

        try:
            capacity = int(capacity) if capacity else 0
        except ValueError:
            capacity = 0

        # Générer la description
        generator = get_event_description_generator()
        creator_name = f"{request.user.first_name} {request.user.last_name}".strip() or request.user.username

        result = generator.generate_description(
            title=title,
            event_type=event_type,
            location=location,
            date=date,
            capacity=capacity,
            creator_name=creator_name,
            tone=tone
        )

        if result['success']:
            return JsonResponse({'success': True, 'description': result['description']})
        else:
            return JsonResponse({'success': False, 'error': result['error']})

    return JsonResponse({'success': False, 'error': 'Méthode non autorisée'})

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
