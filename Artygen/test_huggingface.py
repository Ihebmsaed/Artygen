"""
Script pour tester le nouveau token Hugging Face
"""
import requests
import os
from dotenv import load_dotenv

load_dotenv()


print("=" * 60)
print("TEST DE L'API HUGGING FACE POUR GÉNÉRATION D'IMAGES")
print("=" * 60)

# Lire le token depuis .env
token = os.getenv("HF_TOKEN", "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")

print(f"\n📝 Token utilisé: {token[:15]}...")

# Test avec différents modèles populaires
models = [
    "black-forest-labs/FLUX.1-schnell",
    "stabilityai/stable-diffusion-xl-base-1.0", 
    "prompthero/openjourney",
    "runwayml/stable-diffusion-v1-5",
    "CompVis/stable-diffusion-v1-4"
]

print("\n🔍 Test des modèles disponibles...\n")

working_model = None

for model in models:
    api_url = f"https://api-inference.huggingface.co/models/{model}"
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.post(
            api_url,
            headers=headers,
            json={"inputs": "a beautiful sunset"},
            timeout=10
        )
        
        status = response.status_code
        
        if status == 200:
            print(f"✅ {model}: FONCTIONNE PARFAITEMENT!")
            working_model = model
            break
        elif status == 503:
            print(f"⏳ {model}: Modèle en chargement (peut fonctionner)")
            if not working_model:
                working_model = model
        elif status == 401:
            print(f"🔑 {model}: Token invalide")
        elif status == 404:
            print(f"❌ {model}: Modèle introuvable")
        else:
            print(f"⚠️ {model}: Erreur {status}")
            
    except Exception as e:
        print(f"❌ {model}: Erreur - {str(e)[:50]}")

if working_model:
    print("\n" + "=" * 60)
    print("✅ SUCCÈS!")
    print("=" * 60)
    print(f"\nModèle recommandé à utiliser: {working_model}")
    print(f"\nMettez à jour la ligne 14 de generator/views.py avec:")
    print(f'API_URL = "https://api-inference.huggingface.co/models/{working_model}"')
else:
    print("\n" + "=" * 60)
    print("❌ AUCUN MODÈLE DISPONIBLE")
    print("=" * 60)
    print("\nVérifiez que votre token est valide sur:")
    print("https://huggingface.co/settings/tokens")

