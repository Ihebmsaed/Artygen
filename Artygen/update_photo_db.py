"""
Mettre à jour MANUELLEMENT les chemins de photos dans la base de données
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'artify.settings')
django.setup()

from django.contrib.auth.models import User
from accounts.models import Profile

print("="*70)
print("MISE À JOUR MANUELLE DES CHEMINS DE PHOTOS")
print("="*70)

# Récupérer tous les profils avec photos
profiles = Profile.objects.exclude(photo='')

print(f"\n📊 {profiles.count()} profil(s) avec photo trouvé(s)\n")

for profile in profiles:
    old_path = str(profile.photo)
    filename = os.path.basename(old_path)
    
    print(f"👤 {profile.user.username}")
    print(f"   Ancien: {old_path}")
    print(f"   Nouveau: {filename}")
    
    # Mettre à jour DIRECTEMENT le champ photo
    profile.photo = filename
    profile.save()
    
    # Vérifier
    profile.refresh_from_db()
    print(f"   ✅ Sauvegardé: {profile.photo}")
    print()

print("="*70)
print("TERMINÉ!")
print("="*70)
