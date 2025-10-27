from django.db.models.query import QuerySet
from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.views.decorators.http import require_http_methods
from django.views import View

from .models import Post ,Comment,Favourites
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .forms import FavouriteNoteForm


from django.http import JsonResponse

from random import randint
from django.utils.html import format_html
import os
from dotenv import load_dotenv
from django.contrib import messages

import google.generativeai as genai

# Create your views here.


""" def home(request):
    context={
        'posts':Post.objects.all()
    }
    return render(
        request,
        'Blog/blog.html',context
    )
 """
""" def about (request):
    return HttpResponse("<h1>About</h1>") """
class PostListView(LoginRequiredMixin,ListView):
    model = Post
    template_name = 'Blog/blog.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']  
    
class PostDetailView(LoginRequiredMixin,DetailView):
    model = Post
    template_name = 'Blog/detail.html'
    
class PostDetailViewBlog(LoginRequiredMixin,DetailView):
    model = Post
    template_name = 'Blog/detail_Blog.html'
    


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'Blog/create.html'
    fields = ['title', 'content', 'image']

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, '✅ Post publié avec succès !')
        return super().form_valid(form)

    success_url = reverse_lazy('post-home')
   




       
class UserPostListView(LoginRequiredMixin,ListView):
    model = Post
    template_name = 'Blog/user_posts.html'  # Créez ce template
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user).order_by('-date_posted')

class UserFavouriteListView(LoginRequiredMixin,ListView):
    model = Favourites
    template_name = 'Blog/user_favourites.html' 
    context_object_name = 'favourites'
    
    def get_queryset(self) :
        return Favourites.objects.filter(user=self.request.user).order_by('-added_on')

class favouritesDeleteView (LoginRequiredMixin,DeleteView):
    model = Favourites
    template_name = 'Blog/favourite_confirm_delete.html'  # Créez ce template
    success_url = reverse_lazy('favourites')

""" class UpdatePostView(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ['title', 'content']  # Champs à mettre à jour
    template_name = 'edit_post.html'  # Nom de votre template
    context_object_name = 'post'  # Nom de l'objet dans le template

    def get_success_url(self):
        return reverse_lazy('user-posts')
 """
class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'Blog/post_confirm_delete.html'  # Créez ce template
    success_url = reverse_lazy('user-posts')



@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    if request.method == 'POST':
        # Récupération des données du formulaire
        post.title = request.POST['title']
        post.content = request.POST['content']
        
        # Mise à jour de l'image si présente
        if 'image' in request.FILES:
            post.image = request.FILES['image']
        
        post.save()
        messages.success(request, '✅ Post modifié avec succès !')
        return redirect('user-posts')

    return render(request, 'Blog/edit_post.html', {'post': post})

@login_required
def like_post(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, id=post_id)
        if request.user in post.liked_by.all():
            post.liked_by.remove(request.user)
            post.likes_count -= 1
        else:
            post.liked_by.add(request.user)
            post.likes_count += 1
        post.save()
        return JsonResponse({'likes_count': post.likes_count, 'liked': request.user in post.liked_by.all()})
    
    

@login_required
def add_comment(request, post_id):
    if request.method == 'POST':
        print(request.body)  # Afficher le corps de la requête
        post = get_object_or_404(Post, id=post_id)
        try:
            data = json.loads(request.body)  # Charger le JSON
            content = data.get('content')
            if content:
                Comment.objects.create(post=post, author=request.user, content=content)
                return JsonResponse({'comment': content, 'author': request.user.username})
            else:
                return JsonResponse({'error': 'Content is required'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)




@require_http_methods(["DELETE"])
def delete_comment(request, comment_id):
    try:
        comment = Comment.objects.get(id=comment_id)
        if comment.author == request.user:
            comment.delete()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'error': 'Unauthorized'}, status=403)
    except Comment.DoesNotExist:
        return JsonResponse({'error': 'Comment not found'}, status=404)
    
    
    
    

# Charge les variables d'environnement à partir du fichier .env
load_dotenv()

from django.conf import settings

# Créer la configuration du modèle avec la nouvelle configuration de génération
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

class GenerateTextView(View):
    def __init__(self):
        super().__init__()
        # Essayer d'abord depuis .env, puis depuis settings.py
        api_key = os.getenv("API_KEY") or settings.GEMINI_API_KEY
        if not api_key:
            raise ValueError("API key is not set in .env file or settings.py")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-2.0-flash", generation_config=generation_config)
        self.chat_session = self.model.start_chat(history=[])

    def post(self, request):
        try:
            data = json.loads(request.body)  # Charger les données JSON
            content = data.get('content')
            print("Received POST request")
            print("Content received:", content)

            if content:
                # Formatez le contenu pour demander une reformulation et une correction
             #   formatted_content = f"Veuillez reformuler le texte suivant en améliorant le vocabulaire et en corrigeant les fautes : {content}"
                formatted_content = f"À partir des mots que tu m'as donnés, peux-tu me suggérer une inspiration artistique à poster  : {content}"

                generated_text = self.rephrase_text(formatted_content)
                return JsonResponse({'generated_text': generated_text})
            else:
                return JsonResponse({'error': 'Content is required'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            error_message = str(e)
            print(f"Error during text generation: {error_message}")
            
            # Vérifier si c'est une erreur de quota
            if "429" in error_message or "RATE_LIMIT_EXCEEDED" in error_message or "Quota exceeded" in error_message:
                return JsonResponse({
                    'error': 'Le quota de l\'API Google Gemini a été dépassé. Veuillez réessayer plus tard ou utiliser une autre clé API.'
                }, status=429)
            
            return JsonResponse({'error': error_message}, status=500)

    def rephrase_text(self, text):
        # Envoyer le message d'entrée à la session de chat et obtenir la réponse
        response = self.chat_session.send_message(text)
        return response.text



import requests

        
class SuggestionView(View):
    def __init__(self):
        super().__init__()
        # Essayer d'abord depuis .env, puis depuis settings.py
        api_key = os.getenv("API_KEY") or settings.GEMINI_API_KEY
        if not api_key:
            raise ValueError("API key is not set in .env file or settings.py")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-2.0-flash", generation_config=generation_config)
        self.chat_session = self.model.start_chat(history=[])

    def post(self, request):
        try:
            data = json.loads(request.body)  
            content = data.get('content')  # Récupérer le contenu des données
            print("Received POST request")
            print("Content received:", content)

            if content:
                formatted_content = f"complet le phrase suivant dans un theme artistique {{sugge}} {content}"
                generated_text = self.get_suggestions(formatted_content)  # Appeler la méthode pour obtenir les suggestions
                return JsonResponse({'suggestions': generated_text})
            else:
                return JsonResponse({'error': 'Content is required'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            error_message = str(e)
            print(f"Error during suggestion generation: {error_message}")
            
            # Vérifier si c'est une erreur de quota
            if "429" in error_message or "RATE_LIMIT_EXCEEDED" in error_message or "Quota exceeded" in error_message:
                return JsonResponse({
                    'error': 'Le quota de l\'API Google Gemini a été dépassé. Veuillez réessayer plus tard ou utiliser une autre clé API.'
                }, status=429)
            
            return JsonResponse({'error': error_message}, status=500)

    def get_suggestions(self, text):
        # Envoyer le message d'entrée à la session de chat et obtenir la réponse
        response = self.chat_session.send_message(text)
        return response.text

@csrf_exempt
@login_required
def save_to_favourites(request, post_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            note = data.get('note', '')
            priority = data.get('priority', 'Medium')
            
            # Find the post and create a new favorite entry
            post = Post.objects.get(id=post_id)
            favourite, created = Favourites.objects.get_or_create(
                user=request.user,
                post=post,
                defaults={'note': note, 'priority': priority}
            )
            
            if not created:
                # If it already exists, update the note and priority if desired
                favourite.note = note
                favourite.priority = priority
                favourite.save()
                
            return JsonResponse({'message': 'Favorite saved successfully!' if created else 'Favorite updated successfully!'})

        except Post.DoesNotExist:
            return JsonResponse({'error': 'Post not found.'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request method.'}, status=400)

def blog(request):
    return render(request, 'blog.html')