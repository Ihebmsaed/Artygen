from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.files.base import ContentFile
import requests
import base64
from PIL import Image
import io
import os
from dotenv import load_dotenv
from artwork.models import Artwork
from category.models import Category

# Charger les variables d'environnement
load_dotenv()

# Importer les secrets depuis le fichier local
try:
    from secrets import HUGGINGFACE_TOKEN
except ImportError:
    HUGGINGFACE_TOKEN = os.getenv("HF_TOKEN", "")

# Configuration API
# FLUX.1-schnell : Modèle rapide et de haute qualité pour la génération d'images
API_URL = "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-schnell"
HF_TOKEN = HUGGINGFACE_TOKEN

def query(payload):
    """Envoie une requête à l'API Hugging Face pour générer une image"""
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    
    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=120)
        print("Status Code:", response.status_code)
        print("Response:", response.text[:200] if response.status_code != 200 else "Image OK")
        
        if response.status_code == 503:
            # Le modèle est en cours de chargement
            raise Exception("⏳ Le modèle IA est en cours de chargement. Veuillez réessayer dans 30 secondes.")
        
        if response.status_code == 401:
            raise Exception("🔑 Token API invalide. Veuillez configurer un nouveau token Hugging Face dans le fichier .env (HF_TOKEN)")
        
        if response.status_code == 404:
            raise Exception("❌ Le modèle d'IA n'est pas accessible. Veuillez vérifier la configuration de l'API.")
        
        if response.status_code != 200:
            error_text = response.text
            if "error" in error_text.lower():
                raise Exception(f"Erreur API: {error_text[:200]}")
            raise Exception(f"Erreur {response.status_code}: Impossible de générer l'image. Réessayez plus tard.")
        
        return response.content
    
    except requests.exceptions.Timeout:
        raise Exception("⏱️ Délai d'attente dépassé. Le serveur met trop de temps à répondre. Réessayez.")
    except requests.exceptions.ConnectionError:
        raise Exception("🌐 Erreur de connexion. Vérifiez votre connexion internet.")
    except Exception as e:
        if "Token" in str(e) or "401" in str(e):
            raise Exception("🔑 Token API invalide ou expiré. Obtenez un nouveau token sur: https://huggingface.co/settings/tokens")
        raise

def generate_image(request):
    if request.method == 'POST':
        prompt = request.POST.get('prompt')
        style = request.POST.get('style')  # Get the selected style from the form
        if prompt and style:
            try:
                # Combiner le prompt avec le style pour une meilleure génération
                full_prompt = f"{prompt}, {style} style, high quality, detailed"
                
                # Send the prompt to the API
                image_bytes = query({"inputs": full_prompt})
                
                # Open the image
                image = Image.open(io.BytesIO(image_bytes))
                
                # Convert the image to a format that can be rendered in the template
                img_io = io.BytesIO()
                image.save(img_io, 'PNG')
                img_io.seek(0)
                image_data = base64.b64encode(img_io.read()).decode('utf-8')

                # Render the result template with the image
                categories = Category.objects.all()
                return render(request, 'result.html', {
                    'prompt': prompt,
                    'style': style,
                    'image_data': image_data,
                    'categories': categories,
                })
            except Exception as e:
                return render(request, 'generate_image.html', {
                    'error': str(e),
                })

    return render(request, 'generate_image.html')

@login_required
def save_generated_artwork(request):
    """Sauvegarde l'artwork généré dans la base de données"""
    if request.method == 'POST':
        try:
            # Récupérer les données du formulaire
            image_data = request.POST.get('image_data')
            prompt = request.POST.get('prompt')
            style = request.POST.get('style', '')
            category_id = request.POST.get('category_id')
            
            if not image_data or not prompt:
                messages.error(request, "Données manquantes pour sauvegarder l'artwork.")
                return redirect('generate_image')
            
            # Décoder l'image base64
            image_bytes = base64.b64decode(image_data)
            
            # Créer un nom de fichier unique
            import uuid
            filename = f"ai_generated_{uuid.uuid4()}.png"
            
            # Récupérer ou créer une catégorie par défaut pour les artworks générés par IA
            if category_id:
                category = Category.objects.get(id=category_id)
            else:
                category, created = Category.objects.get_or_create(
                    name="AI Generated",
                    defaults={'description': "Artworks générés par intelligence artificielle"}
                )
            
            # Créer l'artwork
            artwork = Artwork(
                title=f"AI: {prompt[:50]}",  # Limiter le titre à 50 caractères
                description=f"Généré par IA avec le prompt: {prompt}\nStyle: {style}",
                category=category,
                user=request.user,
                tags=f"ai-generated,{style},{prompt}"
            )
            
            # Sauvegarder le fichier image
            artwork.file.save(filename, ContentFile(image_bytes), save=True)
            
            messages.success(request, "🎨 Artwork sauvegardé avec succès !")
            return redirect('artwork_list')
            
        except Exception as e:
            messages.error(request, f"Erreur lors de la sauvegarde: {str(e)}")
            return redirect('generate_image')
    
    return redirect('generate_image')
