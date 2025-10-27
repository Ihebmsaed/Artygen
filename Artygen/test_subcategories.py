"""
Script pour tester l'endpoint de génération de sous-catégories
"""
import requests

print("=" * 60)
print("TEST DE L'ENDPOINT GET_ART_SUBCATEGORIES")
print("=" * 60)

# URL de l'endpoint (avec category_id = 1 comme dans l'erreur)
url = "http://127.0.0.1:8000/category/categories/1/subcategories/get_art_subcategories/"

print(f"\n🔍 Test de: {url}")

try:
    response = requests.get(url, timeout=30)
    
    print(f"\n📊 Status Code: {response.status_code}")
    
    if response.status_code == 200:
        print("✅ SUCCÈS!")
        data = response.json()
        print(f"\n📦 Données reçues:")
        print(f"Nombre de sous-catégories: {len(data.get('subcategories', []))}")
        
        for i, subcat in enumerate(data.get('subcategories', [])[:3], 1):
            print(f"\n{i}. {subcat.get('subcategory')}")
            print(f"   Description: {subcat.get('description', 'N/A')[:80]}...")
    else:
        print(f"❌ ERREUR {response.status_code}")
        print(f"\nRéponse: {response.text[:500]}")
        
except requests.exceptions.ConnectionError:
    print("❌ Impossible de se connecter au serveur")
    print("Assurez-vous que le serveur Django est en cours d'exécution")
except Exception as e:
    print(f"❌ Erreur: {str(e)}")

print("\n" + "=" * 60)
