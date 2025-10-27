"""
Test d'inscription avec photo de profil
"""
import os
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'artify.settings')
django.setup()

from django.contrib.auth.models import User
from accounts.models import Profile
from django.core.files.uploadedfile import SimpleUploadedFile
from accounts.forms import CustomUserCreationForm
from datetime import date

def test_registration_with_photo():
    """
    Teste l'inscription avec upload de photo
    """
    print("\n" + "="*70)
    print("TEST D'INSCRIPTION AVEC PHOTO DE PROFIL")
    print("="*70)
    
    # Utiliser une vraie image de test
    test_image_path = os.path.join(os.path.dirname(__file__), 'test_data', 'test_profile_photo.png')
    
    if not os.path.exists(test_image_path):
        print(f"❌ ERREUR: Image de test introuvable à {test_image_path}")
        print("   Exécutez d'abord: python create_test_image.py")
        return
    
    # Lire le contenu de l'image
    with open(test_image_path, 'rb') as img_file:
        image_content = img_file.read()
    
    test_image = SimpleUploadedFile(
        name='test_photo.png',
        content=image_content,
        content_type='image/png'
    )
    
    print(f"📸 Image de test chargée: {len(image_content)} bytes")
    
    # Données du formulaire
    form_data = {
        'username': 'test_photo_user',
        'first_name': 'Test',
        'last_name': 'PhotoUser',
        'email': 'testphoto@example.com',
        'password1': 'TestPassword123!',
        'password2': 'TestPassword123!',
        'cin': '12345678',
        'birthdate': date(1995, 5, 15),
        'role': 'user',
        'art_style': 'Photographie de paysages',
        'art_interests': 'nature, montagnes, couchers de soleil',
        'generate_bio': True
    }
    
    form_files = {
        'profile_image': test_image
    }
    
    # Supprimer l'utilisateur s'il existe déjà
    User.objects.filter(username='test_photo_user').delete()
    
    print("\n📝 Création du formulaire avec photo...")
    form = CustomUserCreationForm(data=form_data, files=form_files)
    
    if form.is_valid():
        print("✅ Formulaire valide!")
        
        # Sauvegarder l'utilisateur
        user = form.save()
        print(f"✅ Utilisateur créé: {user.username}")
        
        # Vérifier le profil
        try:
            profile = Profile.objects.get(user=user)
            print(f"\n📊 INFORMATIONS DU PROFIL:")
            print(f"   - Username: {user.username}")
            print(f"   - Email: {user.email}")
            print(f"   - CIN: {profile.cin}")
            print(f"   - Birthdate: {profile.birthdate}")
            print(f"   - Art Style: {profile.art_style}")
            print(f"   - Art Interests: {profile.art_interests}")
            print(f"   - Photo: {profile.photo}")
            print(f"   - Photo path: {profile.photo.path if profile.photo else 'None'}")
            
            if profile.photo:
                print("\n🎉 SUCCESS! La photo a été sauvegardée correctement!")
                print(f"   📸 Chemin de la photo: {profile.photo.path}")
                
                # Vérifier si le fichier existe
                if os.path.exists(profile.photo.path):
                    print(f"   ✅ Le fichier existe sur le disque!")
                    print(f"   📏 Taille: {os.path.getsize(profile.photo.path)} bytes")
                else:
                    print(f"   ❌ ERREUR: Le fichier n'existe PAS sur le disque!")
            else:
                print("\n❌ ERREUR: La photo n'a PAS été sauvegardée dans le profil!")
                
        except Profile.DoesNotExist:
            print("❌ ERREUR: Le profil n'a pas été créé!")
            
    else:
        print("❌ Formulaire invalide!")
        print(f"Erreurs: {form.errors}")
    
    print("\n" + "="*70)
    print("FIN DU TEST")
    print("="*70 + "\n")

if __name__ == '__main__':
    test_registration_with_photo()
