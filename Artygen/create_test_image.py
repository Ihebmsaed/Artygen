"""
Créer une vraie image de test pour les tests
"""
from PIL import Image
import os

# Créer un répertoire temporaire pour les tests
test_dir = os.path.join(os.path.dirname(__file__), 'test_data')
os.makedirs(test_dir, exist_ok=True)

# Créer une image de test simple (100x100, rouge)
img = Image.new('RGB', (100, 100), color=(255, 100, 100))
test_image_path = os.path.join(test_dir, 'test_profile_photo.png')
img.save(test_image_path)

print(f"✅ Image de test créée: {test_image_path}")
print(f"📏 Taille: {os.path.getsize(test_image_path)} bytes")
