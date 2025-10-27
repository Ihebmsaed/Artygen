"""
Debug: Tracer exactement ce qui se passe lors de l'inscription
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'artify.settings')
django.setup()

from django.contrib.auth.models import User
from accounts.models import Profile

print("="*60)
print("ÉTAT ACTUEL DE LA BASE DE DONNÉES")
print("="*60)

# Lister les utilisateurs récemment créés
users = User.objects.all().order_by('-id')[:5]

print(f"\n👥 Derniers utilisateurs créés: {users.count()}")
for user in users:
    print(f"\n{'='*40}")
    print(f"Username: {user.username}")
    print(f"Email: {user.email}")
    print(f"Date création: {user.date_joined}")
    
    try:
        profile = user.profile
        print(f"Photo: {profile.photo}")
        print(f"CIN: {profile.cin}")
        print(f"Role: {profile.role}")
        
        if profile.photo:
            photo_path = profile.photo.path
            if os.path.exists(photo_path):
                from PIL import Image
                img = Image.open(photo_path)
                print(f"📸 Dimensions de la photo: {img.size}")
                print(f"📂 Chemin complet: {photo_path}")
    except Exception as e:
        print(f"❌ Erreur récupération profile: {e}")

print("\n" + "="*60)
