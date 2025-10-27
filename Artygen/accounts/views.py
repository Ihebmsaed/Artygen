# accounts/views.py
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from .forms import CustomUserCreationForm
from .bio_generator import get_bio_generator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
import os

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            
            # Sauvegarde de l'utilisateur
            user = form.save()
            
            # 🎨 GÉNÉRATION DE BIO PAR IA si demandée
            if form.cleaned_data.get('generate_bio', False):
                art_style = form.cleaned_data.get('art_style', '')
                art_interests = form.cleaned_data.get('art_interests', '')
                
                if art_style or art_interests:
                    try:
                        bio_generator = get_bio_generator()
                        result = bio_generator.generate_bio(
                            username=username,
                            first_name=user.first_name,
                            last_name=user.last_name,
                            art_style=art_style,
                            art_interests=art_interests,
                            tone='professional'
                        )
                        
                        if result['success']:
                            # Sauvegarder la bio générée
                            user.profile.bio = result['bio']
                            user.profile.bio_generated = True
                            user.profile.save()
                            messages.success(request, '✨ Votre bio de profil a été générée automatiquement par IA!')
                        else:
                            messages.warning(request, '⚠️ La génération automatique de bio a échoué, vous pourrez la créer plus tard.')
                    except Exception as e:
                        print(f"Erreur génération bio: {e}")
                        messages.warning(request, '⚠️ Impossible de générer la bio automatiquement.')
            
            # Authentification et connexion
            user = authenticate(username=username, password=password)
            login(request, user)
            
            messages.success(request, '✅ Inscription réussie ! Bienvenue sur Artygen.')
            
            # Check if the user has the 'admin' role and redirect accordingly
            if user.profile.role == 'admin':
                return redirect('/admin/')  # Redirect to Django's admin interface
            else:
                return redirect('home')  # Replace 'home' with your actual home view
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'accounts/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Check if the user has the 'admin' role and redirect accordingly
            if user.profile.role == 'admin':
                return redirect('/admin/')  # Redirect to Django's admin interface
            else:
                return redirect('profile')  # Redirect to profile for regular users
        else:
            messages.error(request, 'Invalid username or password.')  # Show error message
    return render(request, 'accounts/login.html')

@login_required
def profile(request):
    profile_photo = request.user.profile.photo.url if request.user.profile.photo else None
    return render(request, 'accounts/profile.html', {
        'username': request.user.username,
        'user': request.user,
        'profile_photo': profile_photo,
        'join_date': request.user.date_joined.strftime('%B %d, %Y'),
        'PROFILE_PHOTOS_URL': settings.PROFILE_PHOTOS_URL  # Pass the URL to the template
    })

def user_logout(request):
    logout(request)
    return redirect('home')


@login_required
@require_http_methods(["POST"])
def generate_bio_ajax(request):
    """
    Génère ou régénère la bio de profil via AJAX
    """
    try:
        art_style = request.POST.get('art_style', '')
        art_interests = request.POST.get('art_interests', '')
        tone = request.POST.get('tone', 'professional')
        
        if not art_style and not art_interests:
            return JsonResponse({
                'success': False,
                'error': 'Veuillez fournir au moins votre style artistique ou vos intérêts.'
            })
        
        # Générer la bio
        bio_generator = get_bio_generator()
        result = bio_generator.generate_bio(
            username=request.user.username,
            first_name=request.user.first_name,
            last_name=request.user.last_name,
            art_style=art_style,
            art_interests=art_interests,
            tone=tone
        )
        
        if result['success']:
            # Sauvegarder dans le profil
            profile = request.user.profile
            profile.bio = result['bio']
            profile.art_style = art_style
            profile.art_interests = art_interests
            profile.bio_generated = True
            profile.save()
            
            return JsonResponse({
                'success': True,
                'bio': result['bio'],
                'message': '✨ Votre bio a été générée avec succès!'
            })
        else:
            return JsonResponse({
                'success': False,
                'error': result.get('error', 'Erreur inconnue lors de la génération')
            })
            
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Erreur serveur: {str(e)}'
        })


@login_required
def edit_profile(request):
    """
    Page d'édition du profil avec génération de bio
    """
    profile = request.user.profile
    
    if request.method == 'POST':
        # Mise à jour manuelle du profil
        profile.bio = request.POST.get('bio', profile.bio)
        profile.art_style = request.POST.get('art_style', profile.art_style)
        profile.art_interests = request.POST.get('art_interests', profile.art_interests)
        
        # Photo de profil
        if 'photo' in request.FILES:
            profile.photo = request.FILES['photo']
        
        profile.save()
        messages.success(request, '✅ Profil mis à jour avec succès!')
        return redirect('profile')
    
    return render(request, 'accounts/edit_profile.html', {
        'profile': profile,
        'user': request.user
    })
