"""
Test complet d'inscription avec photo
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'artify.settings')
django.setup()

from django.contrib.auth.models import User
from accounts.models import Profile
from django.core.files.uploadedfile import SimpleUploadedFile
from accounts.forms import CustomUserCreationForm
from datetime import date

def test_full_registration():
    print("\n" + "="*70)
    print("TEST D'INSCRIPTION COMPLÈTE AVEC PHOTO")
    print("="*70)
    
    # Lire l'image de test
    test_image_path = os.path.join(os.path.dirname(__file__), 'test_data', 'test_profile_photo.png')
    
    if not os.path.exists(test_image_path):
        print(f"❌ ERREUR: Image de test introuvable")
        return
    
    with open(test_image_path, 'rb') as img_file:
        image_content = img_file.read()
    
    test_image = SimpleUploadedFile(
        name='my_new_photo.png',
        content=image_content,
        content_type='image/png'
    )
    
    # Supprimer l'utilisateur s'il existe
    username = 'test_final_user'
    User.objects.filter(username=username).delete()
    
    # Données du formulaire
    form_data = {
        'username': username,
        'first_name': 'Test',
        'last_name': 'Final',
        'email': 'testfinal@example.com',
        'password1': 'TestPassword123!',
        'password2': 'TestPassword123!',
        'cin': '99999999',
        'birthdate': date(1990, 1, 1),
        'role': 'user',
        'art_style': 'Art moderne',
        'art_interests': 'sculptures, installations',
        'generate_bio': False  # Pas de bio pour ce test
    }
    
    form_files = {
        'profile_image': test_image
    }
    
    print("\n📝 Création du formulaire...")
    form = CustomUserCreationForm(data=form_data, files=form_files)
    
    if form.is_valid():
        print("✅ Formulaire valide!")
        
        # Sauvegarder
        user = form.save()
        print(f"✅ Utilisateur créé: {user.username}")
        
        # Vérifier immédiatement
        user.refresh_from_db()
        profile = user.profile
        
        print(f"\n📊 RÉSULTATS:")
        print(f"   Username: {user.username}")
        print(f"   Email: {user.email}")
        print(f"   CIN: {profile.cin}")
        print(f"   Art Style: {profile.art_style}")
        print(f"   Photo field: '{profile.photo}'")
        print(f"   Photo bool: {bool(profile.photo)}")
        
        if profile.photo:
            print(f"\n🎉 SUCCESS! La photo a été sauvegardée!")
            print(f"   📸 Nom: {profile.photo.name}")
            print(f"   📂 Chemin: {profile.photo.path}")
            
            if os.path.exists(profile.photo.path):
                print(f"   ✅ Le fichier existe sur le disque!")
                print(f"   📏 Taille: {os.path.getsize(profile.photo.path)} bytes")
            else:
                print(f"   ❌ ERREUR: Le fichier n'existe PAS sur le disque!")
        else:
            print(f"\n❌ ÉCHEC! La photo n'a PAS été sauvegardée!")
            print(f"   cleaned_data avait: {form.cleaned_data.get('profile_image')}")
    else:
        print(f"❌ Formulaire invalide!")
        print(f"Erreurs: {form.errors}")
    
    print("\n" + "="*70)
    print("FIN DU TEST")
    print("="*70 + "\n")

if __name__ == '__main__':
    test_full_registration()
