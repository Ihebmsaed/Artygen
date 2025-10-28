"""
Script pour lister toutes les images stockées sur Cloudinary
"""
import os
import cloudinary
import cloudinary.api
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Configuration Cloudinary
cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME', 'dndkxukvc'),
    api_key=os.getenv('CLOUDINARY_API_KEY', '775151114658655'),
    api_secret=os.getenv('CLOUDINARY_API_SECRET', 'R0qagTNETRX004qijaBYTHLR_eg')
)

def list_all_images():
    """Liste toutes les images sur Cloudinary"""
    try:
        print("📸 Récupération des images depuis Cloudinary...\n")
        
        # Récupérer toutes les ressources (images)
        result = cloudinary.api.resources(
            type="upload",
            resource_type="image",
            max_results=500  # Augmentez si vous avez plus d'images
        )
        
        images = result.get('resources', [])
        
        if not images:
            print("❌ Aucune image trouvée sur Cloudinary")
            return
        
        print(f"✅ {len(images)} image(s) trouvée(s):\n")
        print("-" * 80)
        
        for idx, image in enumerate(images, 1):
            print(f"\n📷 Image #{idx}")
            print(f"   Public ID: {image['public_id']}")
            print(f"   Format: {image['format']}")
            print(f"   Taille: {image['bytes']} bytes ({image['bytes'] / 1024:.2f} KB)")
            print(f"   Dimensions: {image['width']}x{image['height']}")
            print(f"   URL: {image['secure_url']}")
            print(f"   Créée le: {image['created_at']}")
            print("-" * 80)
        
        # Résumé
        total_size = sum(img['bytes'] for img in images)
        print(f"\n📊 RÉSUMÉ:")
        print(f"   Total images: {len(images)}")
        print(f"   Espace utilisé: {total_size / (1024 * 1024):.2f} MB")
        
        return images
        
    except Exception as e:
        print(f"❌ Erreur lors de la récupération des images: {str(e)}")
        return None

def list_by_folder(folder_name=""):
    """Liste les images dans un dossier spécifique"""
    try:
        print(f"📁 Récupération des images du dossier '{folder_name}'...\n")
        
        result = cloudinary.api.resources(
            type="upload",
            resource_type="image",
            prefix=folder_name,
            max_results=500
        )
        
        images = result.get('resources', [])
        
        if not images:
            print(f"❌ Aucune image trouvée dans le dossier '{folder_name}'")
            return
        
        print(f"✅ {len(images)} image(s) trouvée(s):\n")
        
        for idx, image in enumerate(images, 1):
            print(f"{idx}. {image['public_id']} - {image['secure_url']}")
        
        return images
        
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        return None

def get_folders():
    """Liste tous les dossiers sur Cloudinary"""
    try:
        print("📁 Récupération des dossiers...\n")
        
        result = cloudinary.api.root_folders()
        folders = result.get('folders', [])
        
        if not folders:
            print("❌ Aucun dossier trouvé")
            return
        
        print(f"✅ {len(folders)} dossier(s) trouvé(s):\n")
        for folder in folders:
            print(f"   📁 {folder['name']}")
            # Compter les images dans chaque dossier
            try:
                count_result = cloudinary.api.resources(
                    type="upload",
                    resource_type="image",
                    prefix=folder['name'],
                    max_results=1
                )
                count = count_result.get('total_count', 0)
                print(f"      ({count} image(s))")
            except:
                pass
        
        return folders
        
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        return None

if __name__ == "__main__":
    print("=" * 80)
    print("🌥️  CLOUDINARY IMAGE MANAGER")
    print("=" * 80)
    print()
    
    # Menu
    print("Que voulez-vous faire?")
    print("1. Lister toutes les images")
    print("2. Lister les dossiers")
    print("3. Lister les images d'un dossier spécifique")
    print()
    
    choice = input("Votre choix (1/2/3): ").strip()
    
    if choice == "1":
        list_all_images()
    elif choice == "2":
        get_folders()
    elif choice == "3":
        folder = input("Nom du dossier: ").strip()
        list_by_folder(folder)
    else:
        print("❌ Choix invalide")
