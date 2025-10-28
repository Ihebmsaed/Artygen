"""
Configuration Cloudinary pour Django
Ce fichier initialise Cloudinary avec les credentials
"""
import cloudinary
import os

def configure_cloudinary():
    """Configure Cloudinary avec les variables d'environnement"""
    cloudinary.config(
        cloud_name=os.environ.get('CLOUDINARY_CLOUD_NAME', ''),
        api_key=os.environ.get('CLOUDINARY_API_KEY', ''),
        api_secret=os.environ.get('CLOUDINARY_API_SECRET', ''),
        secure=True
    )
    
    # Vérifier la configuration
    if cloudinary.config().cloud_name:
        print(f"✅ Cloudinary configuré: {cloudinary.config().cloud_name}")
    else:
        print("⚠️ Cloudinary non configuré - variables d'environnement manquantes")
    
    return cloudinary.config().cloud_name is not None
