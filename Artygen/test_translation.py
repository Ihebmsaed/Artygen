"""
Script de test de la fonctionnalité de traduction du blog
"""
import os
import sys
import django

# Configuration de Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'artify.settings')
django.setup()

from blog.models import Post
from blog.ai_services import TranslationService, process_post_with_ai
from django.contrib.auth.models import User

def test_translation_service():
    """Test du service de traduction"""
    print("\n" + "="*60)
    print("TEST DU SERVICE DE TRADUCTION")
    print("="*60)
    
    # Test simple de traduction
    print("\n1. Test de traduction FR → EN")
    try:
        result = TranslationService.translate_post(
            title="Inspiration Artistique",
            content="Ceci est un test de traduction pour le blog artistique.",
            target_language='en',
            source_language='fr'
        )
        print(f"✅ Titre traduit: {result['title']}")
        print(f"✅ Contenu traduit: {result['content']}")
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False
    
    print("\n2. Test de traduction FR → AR")
    try:
        result = TranslationService.translate_post(
            title="Inspiration Artistique",
            content="Ceci est un test de traduction pour le blog artistique.",
            target_language='ar',
            source_language='fr'
        )
        print(f"✅ Titre traduit: {result['title']}")
        print(f"✅ Contenu traduit: {result['content']}")
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False
    
    print("\n3. Test de traduction FR → ES")
    try:
        result = TranslationService.translate_post(
            title="Inspiration Artistique",
            content="Ceci est un test de traduction pour le blog artistique.",
            target_language='es',
            source_language='fr'
        )
        print(f"✅ Titre traduit: {result['title']}")
        print(f"✅ Contenu traduit: {result['content']}")
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False
    
    return True

def test_post_processing():
    """Test du traitement complet d'un post"""
    print("\n" + "="*60)
    print("TEST DU TRAITEMENT COMPLET D'UN POST")
    print("="*60)
    
    # Récupérer un post existant ou en créer un pour le test
    posts = Post.objects.all()
    
    if posts.exists():
        post = posts.first()
        print(f"\n📝 Post sélectionné: {post.title}")
        print(f"   Auteur: {post.author.username}")
        
        print("\n🔄 Traitement du post avec IA...")
        try:
            result = process_post_with_ai(post)
            
            print("\n✅ RÉSULTATS:")
            print(f"   Sentiment: {result['sentiment']['label']} (score: {result['sentiment']['score']})")
            print(f"   Approprié: {result['moderation']['is_appropriate']}")
            
            # Vérifier les traductions
            print("\n🌍 TRADUCTIONS:")
            if post.title_en:
                print(f"   🇬🇧 EN: {post.title_en[:50]}...")
            if post.title_ar:
                print(f"   🇸🇦 AR: {post.title_ar[:50]}...")
            if post.title_es:
                print(f"   🇪🇸 ES: {post.title_es[:50]}...")
            
            return True
            
        except Exception as e:
            print(f"❌ Erreur lors du traitement: {e}")
            import traceback
            traceback.print_exc()
            return False
    else:
        print("⚠️  Aucun post trouvé dans la base de données")
        print("   Créez un post via l'interface web puis relancez ce test")
        return False

def check_existing_translations():
    """Vérifier les posts existants avec traductions"""
    print("\n" + "="*60)
    print("VÉRIFICATION DES POSTS AVEC TRADUCTIONS")
    print("="*60)
    
    # Posts avec traductions
    posts_with_translations = Post.objects.filter(
        title_en__isnull=False
    ).exclude(title_en='')
    
    print(f"\n📊 Nombre de posts avec traductions: {posts_with_translations.count()}")
    
    if posts_with_translations.exists():
        for post in posts_with_translations[:5]:  # Afficher les 5 premiers
            print(f"\n📝 {post.title}")
            print(f"   🇫🇷 FR: {post.title}")
            if post.title_en:
                print(f"   🇬🇧 EN: {post.title_en}")
            if post.title_ar:
                print(f"   🇸🇦 AR: {post.title_ar}")
            if post.title_es:
                print(f"   🇪🇸 ES: {post.title_es}")
    
    return True

def main():
    """Fonction principale"""
    print("\n" + "="*60)
    print("TEST DE LA FONCTIONNALITÉ DE TRADUCTION DU BLOG")
    print("="*60)
    
    results = []
    
    # Test 1: Service de traduction
    results.append(("Service de traduction", test_translation_service()))
    
    # Test 2: Traitement complet
    results.append(("Traitement complet d'un post", test_post_processing()))
    
    # Test 3: Vérification des posts existants
    results.append(("Vérification des traductions existantes", check_existing_translations()))
    
    print("\n" + "="*60)
    print("RÉSUMÉ DES TESTS")
    print("="*60)
    
    for name, status in results:
        status_icon = "✅" if status else "❌"
        print(f"{status_icon} {name}")
    
    all_ok = all(status for _, status in results)
    
    if all_ok:
        print("\n✅ TOUS LES TESTS SONT PASSÉS!")
        print("La fonctionnalité de traduction est opérationnelle.")
    else:
        print("\n⚠️  CERTAINS TESTS ONT ÉCHOUÉ")
        print("Vérifiez les erreurs ci-dessus.")
    
    print("\n" + "="*60)
    print("INSTRUCTIONS:")
    print("="*60)
    print("1. Pour tester la traduction en ligne:")
    print("   - Créez un nouveau post via l'interface web")
    print("   - Le post sera automatiquement traduit en 4 langues")
    print("\n2. Pour voir les traductions d'un post:")
    print("   - Cliquez sur un post pour le voir en détail")
    print("   - Utilisez les boutons 🇫🇷 🇬🇧 🇸🇦 🇪🇸 en haut")
    print("\n3. Pour retraduire un post existant:")
    print("   - Accédez au dashboard admin de modération")
    print("   - Utilisez le bouton 'Re-analyser'")
    print("="*60)

if __name__ == "__main__":
    main()
