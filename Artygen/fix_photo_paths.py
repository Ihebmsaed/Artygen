"""
Corriger les chemins de photos en double (profile_photos/profile_photos -> profile_photos)
"""
import os
import shutil
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'artify.settings')
django.setup()

from django.contrib.auth.models import User
from accounts.models import Profile


print("="*70)
print("CORRECTION DES CHEMINS DE PHOTOS")
print("="*70)

# Chemin de base
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WRONG_DIR = os.path.join(BASE_DIR, 'profile_photos', 'profile_photos')
CORRECT_DIR = os.path.join(BASE_DIR, 'profile_photos')

print(f"\nRépertoire incorrect: {WRONG_DIR}")
print(f"Répertoire correct: {CORRECT_DIR}")

# Vérifier si le répertoire incorrect existe
if os.path.exists(WRONG_DIR):
    print(f"\n✅ Répertoire incorrect trouvé!")
    
    # Lister les fichiers
    files = [f for f in os.listdir(WRONG_DIR) if os.path.isfile(os.path.join(WRONG_DIR, f))]
    print(f"📁 {len(files)} fichier(s) trouvé(s): {files[:5]}...")
    
    # Déplacer les fichiers
    moved = 0
    for filename in files:
        old_path = os.path.join(WRONG_DIR, filename)
        new_path = os.path.join(CORRECT_DIR, filename)
        
        # Si le fichier existe déjà dans le bon dossier, on le garde
        if not os.path.exists(new_path):
            shutil.move(old_path, new_path)
            moved += 1
            print(f"   ✅ Déplacé: {filename}")
        else:
            print(f"   ⚠️ Déjà existant: {filename}")
    
    print(f"\n📦 {moved} fichier(s) déplacé(s)")
    
    # Supprimer le répertoire incorrect s'il est vide
    try:
        os.rmdir(WRONG_DIR)
        print(f"🗑️ Répertoire incorrect supprimé: {WRONG_DIR}")
    except OSError:
        print(f"⚠️ Le répertoire n'est pas vide, non supprimé")
else:
    print("\n⚠️ Répertoire incorrect introuvable (c'est bon signe!)")

# Mettre à jour la base de données
print("\n" + "="*70)
print("MISE À JOUR DE LA BASE DE DONNÉES")
print("="*70)

users_with_photos = Profile.objects.exclude(photo='')
updated = 0

for profile in users_with_photos:
    old_photo_path = str(profile.photo)
    
    # Si le chemin contient 'profile_photos/profile_photos'
    if 'profile_photos/profile_photos/' in old_photo_path:
        # Extraire juste le nom du fichier
        filename = os.path.basename(old_photo_path)
        new_photo_path = filename
        
        # Mettre à jour
        profile.photo = new_photo_path
        profile.save()
        updated += 1
        
        print(f"✅ {profile.user.username}: {old_photo_path} -> {new_photo_path}")

print(f"\n📊 {updated} profil(s) mis à jour")

print("\n" + "="*70)
print("FIN DE LA CORRECTION")
print("="*70)
