from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Category,Subcategory
from .forms import CategoryForm, SubcategoryForm
from .serializers import SubcategorySerializer
from django.conf import settings
from django.shortcuts import render, get_object_or_404
import requests
from artify.settings import GEMINI_API_KEY
import os
from dotenv import load_dotenv
from requests import post, exceptions
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

# Charger les variables d'environnement
load_dotenv()

# List all categories

@login_required
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'category_list.html', {'categories': categories})

def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)  # Add request.FILES here
        if form.is_valid():
            form.save()
            return redirect('category-list')
    else:
        form = CategoryForm()
    return render(request, 'category_form.html', {'form': form})

def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES, instance=category)  # Add request.FILES here
        if form.is_valid():
            form.save()
            return redirect('category-list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'category_form.html', {'form': form})

# Delete a category
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        return redirect('category-list')
    return render(request, 'category_delete.html', {'category': category})

@login_required
def subcategory_list(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    subcategories = Subcategory.objects.filter(category=category)

    if request.method == 'POST':
        try:
            generated_subcategories = generate_subcategories(category.name)
            for name in generated_subcategories:
                Subcategory.objects.get_or_create(name=name, category=category)
            subcategories = Subcategory.objects.filter(category=category)  # Refresh
        except exceptions.RequestException as e:
            error_message = f"Error generating subcategories: {str(e)}"
            # Handle error, e.g., display message to user
    error_message = ''
    return render(request, 'subcategory_list.html', {
        'category': category,
        'subcategories': subcategories,
        'error_message': error_message if error_message else None,
    })

def generate_subcategories(category_name):
    url = "https://gemini.googleapis.com/v1/models/gemini-pro:generateContent"  # Endpoint without API key
    headers = {
        "Authorization": f"Bearer {GEMINI_API_KEY}",  # Use API key from settings
        "Content-Type": "application/json"
    }
    payload = {
        "prompt": f"Generate subcategories for the category '{category_name}'.",
        "max_tokens": 50
    }
   

    response = post(url, headers=headers, json=payload)
    print(response)
    response.raise_for_status()

    subcategories = response.json().get('subcategories', [])
    return [subcategory.strip() for subcategory in subcategories]

# List all subcategories for a specific category
def subcategory_list(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    subcategories = Subcategory.objects.filter(category=category)
    return render(request, 'subcategory_list.html', {
        'category': category,
        'subcategories': subcategories,
    })

# Create a new subcategory
@csrf_exempt
def subcategory_create(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == 'POST':
        # Vérifier si c'est une requête AJAX (depuis le JavaScript)
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or 'application/json' in request.headers.get('Accept', ''):
            # Traiter comme une requête AJAX
            name = request.POST.get('name')
            description = request.POST.get('description', '')
            
            if name:
                try:
                    subcategory = Subcategory.objects.create(
                        name=name,
                        description=description,
                        category=category
                    )
                    return JsonResponse({
                        'success': True,
                        'message': 'Subcategory added successfully',
                        'subcategory': {
                            'id': subcategory.id,
                            'name': subcategory.name,
                            'description': subcategory.description
                        }
                    })
                except Exception as e:
                    return JsonResponse({'success': False, 'error': str(e)}, status=400)
            else:
                return JsonResponse({'success': False, 'error': 'Name is required'}, status=400)
        else:
            # Traiter comme un formulaire normal
            form = SubcategoryForm(request.POST)
            if form.is_valid():
                subcategory = form.save(commit=False)
                subcategory.category = category
                subcategory.save()
                return redirect('subcategory-list', category_id=category.id)
    else:
        form = SubcategoryForm()
    return render(request, 'subcategory_form.html', {'form': form, 'category': category})

# Update a subcategory
def subcategory_update(request, category_id, pk):
    category = get_object_or_404(Category, id=category_id)
    subcategory = get_object_or_404(Subcategory, pk=pk)
    if request.method == 'POST':
        form = SubcategoryForm(request.POST, instance=subcategory)
        if form.is_valid():
            form.save()
            return redirect('subcategory-list', category_id=category.id)
    else:
        form = SubcategoryForm(instance=subcategory)
    return render(request, 'subcategory_form.html', {'form': form, 'category': category})

# Delete a subcategory
def subcategory_delete(request, category_id, pk):
    category = get_object_or_404(Category, id=category_id)
    subcategory = get_object_or_404(Subcategory, pk=pk)
    if request.method == 'POST':
        subcategory.delete()
        return redirect('subcategory-list', category_id=category.id)
    return render(request, 'subcategory_delete.html', {'subcategory': subcategory, 'category': category})


import google.generativeai as genai
from django.conf import settings

@csrf_exempt
def get_art_subcategories(request, category_id):
    try:
        # Configure the API key from .env or settings.py
        api_key = os.getenv("API_KEY") or settings.GEMINI_API_KEY
        if not api_key:
            return JsonResponse({'error': 'API key not configured'}, status=500)
        
        genai.configure(api_key=api_key)

        # Create a Gemini model instance with the new model
        model = genai.GenerativeModel('gemini-2.0-flash')

        # Retrieve the category by ID
        category = Category.objects.get(id=category_id)
        category_name = category.name

        # Improved prompt to get a structured format
        prompt = f"""List exactly 5 subcategories for the artistic category '{category_name}'.
For each subcategory, provide the name and a brief description on the same line.
Strict format (one per line):
Subcategory Name: Short description

Example:
Portraits: Artistic representations of people
Landscapes: Natural or urban scenes

Now generate the 5 subcategories for '{category_name}'."""

        # Generate the response
        response = model.generate_content(prompt)
        print("Gemini Response:", response.text)

        # Process the response and extract subcategories and descriptions
        subcategories = []
        lines = response.text.split('\n')
        
        for line in lines:
            line = line.strip()
            
            # Ignore empty lines, titles and numbers
            if not line:
                continue
            if line.startswith('#'):
                continue
            if line.lower().startswith('voici'):
                continue
            if line.lower().startswith('exemple'):
                continue
                
            # Remove numbers at the beginning (1., 2., *, -, etc.)
            line = line.lstrip('0123456789.*- ')
            
            # Try to parse with ':'
            if ':' in line:
                parts = line.split(':', 1)
                subcategory = parts[0].strip().replace('**', '').replace('*', '').strip()
                description = parts[1].strip() if len(parts) > 1 else ''
                
                # Check that it's not empty and not too long (probably not a title)
                if subcategory and len(subcategory) < 100 and description:
                    subcategories.append({
                        'subcategory': subcategory,
                        'description': description
                    })
                    
                    # Limit to 5 subcategories
                    if len(subcategories) >= 5:
                        break

        # If no subcategories were found with the expected format
        if not subcategories:
            # Return the raw response for debug
            return JsonResponse({
                'subcategories': [{
                    'subcategory': f'Unparsed response for {category_name}',
                    'description': response.text[:200]
                }]
            })

        # Return the subcategories and descriptions as a JSON response
        return JsonResponse({'subcategories': subcategories})
    
    except Category.DoesNotExist:
        return JsonResponse({'error': 'Category not found'}, status=404)
    except Exception as e:
        print(f"Error in get_art_subcategories: {str(e)}")
        return JsonResponse({'error': f'Internal server error: {str(e)}'}, status=500)