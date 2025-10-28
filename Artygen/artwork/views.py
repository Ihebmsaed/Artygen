from django.shortcuts import render, get_object_or_404, redirect
from .models import Artwork, ArtCollection
from category.models import Category
from .forms import ArtworkForm, ArtCollectionForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages


def artwork_list(request):
    search_query = request.GET.get('search', '') 
    artworks = Artwork.objects.filter(user=request.user) 
    if search_query:  
        artworks = artworks.filter(tags__icontains=search_query)  

    categories = Category.objects.all()
    context = {
        'artworks': artworks,
        'search_query': search_query,
        'categories': categories,
    }
    return render(request, 'artwork/artwork_list.html', context)


def artwork_detail(request, pk):
    artwork = get_object_or_404(Artwork, pk=pk)
    return render(request, 'artwork/artwork_detail.html', {'artwork': artwork})

@login_required 
def artwork_create(request):
    if request.method == 'POST':
        form = ArtworkForm(request.POST, request.FILES)
        if form.is_valid():
            artwork = form.save(commit=False) 
            artwork.user = request.user  
            artwork.save()  
            
            messages.success(request, "✅ New artwork added successfully!")
            
            return redirect('artwork_list')
    else:
        form = ArtworkForm()
    return render(request, 'artwork/artwork_form.html', {'form': form})

@login_required  
def artwork_update(request, pk):
    artwork = get_object_or_404(Artwork, pk=pk)

    if artwork.user != request.user:
        return redirect('artwork_list')

    if request.method == 'POST':
        form = ArtworkForm(request.POST, request.FILES, instance=artwork)
        if form.is_valid():
            form.save()  
            messages.success(request, '✅ The artwork has been modified successfully.')  
            return redirect('artwork_list')  
    else:
        form = ArtworkForm(instance=artwork)

    return render(request, 'artwork/artwork_form.html', {'form': form})

@login_required 
def artwork_delete(request, pk):
    artwork = get_object_or_404(Artwork, pk=pk)

    if artwork.user != request.user:
        return redirect('artwork_list')
    if request.method == 'POST':
        artwork.delete() 
        messages.success(request, 'The artwork has been deleted successfully.')  
        return redirect('artwork_list')  

    return render(request, 'artwork/artwork_confirm_delete.html', {'artwork': artwork})

def all_artworks(request):
    search_query = request.GET.get('search', '')  
    artworks = Artwork.objects.all() 

    if search_query: 
        artworks = artworks.filter(tags__icontains=search_query) 

    return render(request, 'artwork/all_artworks.html', {
        'artworks': artworks,
        'search_query': search_query,  
    })
def artwork_public_detail(request, pk):
    artwork = get_object_or_404(Artwork, pk=pk)
    return render(request, 'artwork/artwork_public_detail.html', {'artwork': artwork})

def add_to_gallery(request, artwork_id):
    artwork = get_object_or_404(Artwork, id=artwork_id)
    galleries = ArtCollection.objects.filter(user=request.user)

    if request.method == 'POST':
        if request.POST.get('action') == 'create_gallery':
            form = ArtCollectionForm(request.POST)
            if form.is_valid():
                new_collection = form.save(commit=False)
                new_collection.user = request.user
                new_collection.save()
                new_collection.artworks.add(artwork)
                messages.success(request, "The artwork has been added to the gallery successfully!")
                return redirect('http://127.0.0.1:8000/artwork/all/')
        else:
            selected_gallery = request.POST.get('gallery')
            if selected_gallery:
                gallery = get_object_or_404(ArtCollection, id=selected_gallery)
                gallery.artworks.add(artwork)
                messages.success(request, "The artwork has been added to the gallery successfully!")
                return redirect('http://127.0.0.1:8000/artwork/all/')

    form = ArtCollectionForm()
    return render(request, 'artwork/add_to_gallery.html', {
        'artwork': artwork,
        'galleries': galleries,
        'form': form
    })

    @login_required  
    def collection_detail(request, pk):
        gallery = get_object_or_404(ArtCollection, pk=pk)
        return render(request, 'artwork/gallery_detail.html', {'gallery': gallery})

def collection_list(request):
    if request.method == 'POST' and request.user.is_authenticated:
        # Create a new collection
        name = request.POST.get('name')
        description = request.POST.get('description', '')
        
        if name:
            ArtCollection.objects.create(
                name=name,
                user=request.user
            )
            messages.success(request, f'Collection "{name}" created successfully!')
        else:
            messages.error(request, 'Collection name is required.')
        
        return redirect('collection_list')
    
    if request.user.is_authenticated:
        galleries = ArtCollection.objects.filter(user=request.user)
    else:
        galleries = []  

    return render(request, 'artwork/gallery_list.html', {'galleries': galleries})

@login_required  
def collection_detail(request, gallery_id):
    gallery = get_object_or_404(ArtCollection, id=gallery_id)

    if request.method == 'POST':
        artwork_id = request.POST.get('artwork_id')
        artwork = get_object_or_404(Artwork, id=artwork_id)

        if artwork.user == request.user and artwork in gallery.artworks.all():
            gallery.artworks.remove(artwork)

            return redirect('collection_detail', gallery_id=gallery.id)

    return render(request, 'artwork/gallery_detail.html', {'gallery': gallery})


@login_required
def remove_artwork_from_gallery(request, gallery_id, artwork_id):
    gallery = get_object_or_404(ArtCollection, id=gallery_id)
    artwork = get_object_or_404(Artwork, id=artwork_id)

    if gallery.user != request.user:
        return redirect('collection_list') 

    gallery.artworks.remove(artwork)
    
    messages.success(request, 'The artwork has been removed from the gallery successfully.')

    return redirect('collection_detail', gallery_id=gallery.id) 

@login_required  
def collection_delete(request, gallery_id):
    gallery = get_object_or_404(ArtCollection, id=gallery_id)

    if gallery.user != request.user:
        return redirect('collection_list') 

    if request.method == 'POST':
        gallery.delete()
        messages.success(request, 'The gallery has been deleted successfully.')  
        return redirect('collection_list')  

    return render(request, 'artwork/gallery_confirm_delete.html', {'gallery': gallery})