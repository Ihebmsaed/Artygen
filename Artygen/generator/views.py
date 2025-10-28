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
    from secrets_config import HUGGINGFACE_TOKEN
    HF_TOKEN = HUGGINGFACE_TOKEN
    print("✅ Loaded HF_TOKEN from secrets_config")
except ImportError:
    HF_TOKEN = os.getenv("HF_TOKEN", "")
    print(f"⚠️ Loaded HF_TOKEN from environment: {'✅ Found' if HF_TOKEN else '❌ MISSING'}")

if not HF_TOKEN:
    print("🚨 WARNING: HF_TOKEN is not configured!")

# Configuration API
# FLUX.1-schnell : Modèle rapide et de haute qualité pour la génération d'images
API_URL = "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-schnell"

def query(payload):
    """Send a request to the Hugging Face API to generate an image"""
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    
    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=120)
        print("Status Code:", response.status_code)
        print("Response:", response.text[:200] if response.status_code != 200 else "Image OK")
        
        if response.status_code == 503:
            # The model is loading
            raise Exception("⏳ The AI model is loading. Please try again in 30 seconds.")
        
        if response.status_code == 401:
            raise Exception("🔑 Invalid API token. Please configure a new Hugging Face token in the .env file (HF_TOKEN)")
        
        if response.status_code == 404:
            raise Exception("❌ The AI model is not accessible. Please check the API configuration.")
        
        if response.status_code != 200:
            error_text = response.text
            if "error" in error_text.lower():
                raise Exception(f"API Error: {error_text[:200]}")
            raise Exception(f"Error {response.status_code}: Unable to generate image. Please try again later.")
        
        return response.content
    
    except requests.exceptions.Timeout:
        raise Exception("⏱️ Timeout exceeded. The server is taking too long to respond. Please try again.")
    except requests.exceptions.ConnectionError:
        raise Exception("🌐 Connection error. Please check your internet connection.")
    except Exception as e:
        if "Token" in str(e) or "401" in str(e):
            raise Exception("🔑 Invalid or expired API token. Get a new token at: https://huggingface.co/settings/tokens")
        raise

def generate_image(request):
    # Check if HF_TOKEN is configured
    if not HF_TOKEN:
        return render(request, 'generate_image.html', {
            'error': '🔑 Hugging Face API token is not configured. Please add HF_TOKEN to environment variables on Render.',
        })
    
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
    """Save the generated artwork to the database"""
    if request.method == 'POST':
        try:
            # Get form data
            image_data = request.POST.get('image_data')
            prompt = request.POST.get('prompt')
            style = request.POST.get('style', '')
            category_id = request.POST.get('category_id')
            
            if not image_data or not prompt:
                messages.error(request, "Missing data to save the artwork.")
                return redirect('generate_image')
            
            # Decode base64 image
            image_bytes = base64.b64decode(image_data)
            
            # Create a unique filename
            import uuid
            filename = f"ai_generated_{uuid.uuid4()}.png"
            
            # Get or create a default category for AI-generated artworks
            if category_id:
                category = Category.objects.get(id=category_id)
            else:
                category, created = Category.objects.get_or_create(
                    name="AI Generated",
                    defaults={'description': "Artworks generated by artificial intelligence"}
                )
            
            # Create the artwork
            artwork = Artwork(
                title=f"AI: {prompt[:50]}",  # Limit title to 50 characters
                description=f"Generated by AI with prompt: {prompt}\nStyle: {style}",
                category=category,
                user=request.user,
                tags=f"ai-generated,{style},{prompt}"
            )
            
            # Save the image file
            artwork.file.save(filename, ContentFile(image_bytes), save=True)
            
            messages.success(request, "🎨 Artwork saved successfully!")
            return redirect('artwork_list')
            
        except Exception as e:
            messages.error(request, f"Error during saving: {str(e)}")
            return redirect('generate_image')
    
    return redirect('generate_image')
