"""
Vérifier les détails de l'utilisateur gakpo
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'artify.settings')
django.setup()

from django.contrib.auth.models import User
from accounts.models import Profile

try:
    user = User.objects.get(username='gakpo')
    profile = user.profile
    
    print("="*60)
    print(f"DÉTAILS DE L'UTILISATEUR: {user.username}")
    print("="*60)
    print(f"Email: {user.email}")
    print(f"Date création: {user.date_joined}")
    print(f"\n--- PROFIL ---")
    print(f"Photo field: '{profile.photo}'")
    print(f"Photo bool: {bool(profile.photo)}")
    
    if profile.photo:
        print(f"Photo name: {profile.photo.name}")
        print(f"Photo path: {profile.photo.path}")
        print(f"File exists: {os.path.exists(profile.photo.path)}")
        if os.path.exists(profile.photo.path):
            print(f"File size: {os.path.getsize(profile.photo.path)} bytes")
    else:
        print("⚠️ AUCUNE PHOTO dans la base de données!")
    
    print(f"\nArt Style: {profile.art_style}")
    print(f"Art Interests: {profile.art_interests}")
    print(f"Bio: {profile.bio[:100] if profile.bio else 'None'}...")
    print("="*60)
    
except User.DoesNotExist:
    print("❌ Utilisateur 'gakpo' introuvable!")
