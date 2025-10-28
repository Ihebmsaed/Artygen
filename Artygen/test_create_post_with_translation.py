"""
Script pour tester la création d'un post avec traduction automatique
"""
import os
import sys
import django

# Configuration de Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'artify.settings')
django.setup()

from blog.models import Post
from blog.ai_services import process_post_with_ai
from django.contrib.auth.models import User

def create_test_post():
    """Crée un post de test avec traduction"""
    print("\n" + "="*60)
    print("CRÉATION D'UN POST DE TEST AVEC TRADUCTION AUTOMATIQUE")
    print("="*60)
    
    # Récupérer un utilisateur
    try:
        user = User.objects.first()
        if not user:
            print("❌ Aucun utilisateur trouvé. Créez un utilisateur d'abord.")
            return False
        
        print(f"\n👤 Utilisateur: {user.username}")
        
        # Créer le post
        post = Post.objects.create(
            title="Test de Traduction Automatique",
            content="Ceci est un post de test pour vérifier que la traduction automatique fonctionne correctement. Le système devrait traduire ce texte en anglais, arabe et espagnol.",
            author=user,
            original_language='fr'
        )
        
        print(f"\n✅ Post créé avec ID: {post.id}")
        print(f"   Titre: {post.title}")
        print(f"   Langue originale: {post.original_language}")
        
        # Traiter le post avec IA
        print("\n🤖 Traitement avec IA en cours...")
        print("   - Analyse de sentiment")
        print("   - Modération")
        print("   - Traduction en 4 langues")
        
        try:
            result = process_post_with_ai(post)
            
            print("\n✅ TRAITEMENT TERMINÉ !")
            
            # Afficher les résultats
            print("\n" + "="*60)
            print("RÉSULTATS DE L'ANALYSE IA")
            print("="*60)
            
            # Sentiment
            print(f"\n😊 Sentiment:")
            print(f"   Label: {result['sentiment']['label']}")
            print(f"   Score: {result['sentiment']['score']:.2f}")
            print(f"   Confiance: {result['sentiment']['confidence']:.2f}")
            
            # Modération
            print(f"\n⚠️  Modération:")
            print(f"   Approprié: {result['moderation']['is_appropriate']}")
            if not result['moderation']['is_appropriate']:
                print(f"   Raison: {result['moderation']['reason']}")
            
            # Traductions
            print(f"\n🌍 Traductions:")
            print(f"\n   🇫🇷 FRANÇAIS (original):")
            print(f"      Titre: {post.title}")
            print(f"      Contenu: {post.content[:80]}...")
            
            if post.title_en:
                print(f"\n   🇬🇧 ANGLAIS:")
                print(f"      Titre: {post.title_en}")
                print(f"      Contenu: {post.content_en[:80]}...")
            
            if post.title_ar:
                print(f"\n   🇸🇦 ARABE:")
                print(f"      Titre: {post.title_ar}")
                print(f"      Contenu: {post.content_ar[:80]}...")
            
            if post.title_es:
                print(f"\n   🇪🇸 ESPAGNOL:")
                print(f"      Titre: {post.title_es}")
                print(f"      Contenu: {post.content_es[:80]}...")
            
            print("\n" + "="*60)
            print("✅ LE POST A ÉTÉ TRADUIT AVEC SUCCÈS !")
            print("="*60)
            print(f"\nAccédez au post sur : http://127.0.0.1:8000/blog/post_Blog/{post.id}/")
            print("Utilisez les boutons 🇫🇷 🇬🇧 🇸🇦 🇪🇸 pour basculer entre les langues")
            
            return True
            
        except Exception as e:
            print(f"\n❌ Erreur lors du traitement IA: {e}")
            import traceback
            traceback.print_exc()
            
            # Supprimer le post en cas d'erreur
            post.delete()
            print("   Post supprimé")
            return False
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Fonction principale"""
    print("\n" + "="*60)
    print("SCRIPT DE TEST DE TRADUCTION AUTOMATIQUE")
    print("="*60)
    
    success = create_test_post()
    
    if success:
        print("\n✅ TEST RÉUSSI !")
        print("La traduction automatique fonctionne correctement.")
    else:
        print("\n❌ TEST ÉCHOUÉ")
        print("Vérifiez les erreurs ci-dessus.")
    
    print("\n" + "="*60)

if __name__ == "__main__":
    main()
