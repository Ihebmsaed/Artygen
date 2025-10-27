# gallery/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Gallery
from .forms import GalleryForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def gallery_list(request):
    galleries = Gallery.objects.all()
    return render(request, 'gallery/gallery_list.html', {'galleries': galleries})

@login_required
def gallery_create(request):
    if request.method == "POST":
        print(request.POST)  # To see the posted data
        form = GalleryForm(request.POST)
        print(form.errors)  # To see any form errors
        if form.is_valid():
            gallery = form.save(commit=False)
            gallery.owner = request.user  # Set the current user as the owner
            gallery.save()
            return redirect('gallery_list')  # Redirect to the gallery list
    else:
        form = GalleryForm()
    return render(request, 'gallery/gallery_form.html', {'form': form})

@login_required
def gallery_update(request, pk):
    gallery = get_object_or_404(Gallery, pk=pk)
    if request.method == "POST":
        form = GalleryForm(request.POST, instance=gallery)
        if form.is_valid():
            form.save()
            return redirect('my_galleries')  # Redirect to the gallery list
    else:
        form = GalleryForm(instance=gallery)
    return render(request, 'gallery/gallery_form.html', {'form': form})

@login_required
def gallery_delete(request, pk):
    gallery = get_object_or_404(Gallery, pk=pk)  # Get the gallery object by primary key
    gallery.delete()  # Delete the gallery object
    messages.success(request, 'Gallery deleted successfully.')  # Add success message
    return redirect('my_galleries')  # Redirect to the my galleries page


def my_galleries(request):
    user_galleries = Gallery.objects.filter(owner=request.user)
    if not user_galleries.exists():
        return render(request, 'gallery/my_galleries.html', {'message': "You don't have any galleries yet."})
    return render(request, 'gallery/my_galleries.html', {'galleries': user_galleries})
