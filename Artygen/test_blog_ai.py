"""
Script de test pour les fonctionnalités IA du blog
Usage: python test_blog_ai.py
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'artify.settings')
django.setup()

from blog.ai_services import TranslationService, SentimentModerationService

def test_translation():
    """Test de traduction"""
    print("\n=== TEST DE TRADUCTION ===")
    
    title = "J'adore l'art moderne"
    content = "Cette exposition était magnifique, j'ai adoré chaque œuvre d'art."
    
    print(f"Texte original (FR):")
    print(f"  Titre: {title}")
    print(f"  Contenu: {content}")
    
    # Traduire en anglais
    print("\n🇬🇧 Traduction en anglais...")
    translation_en = TranslationService.translate_post(title, content, target_language='en')
    print(f"  Titre: {translation_en['title']}")
    print(f"  Contenu: {translation_en['content']}")
    
    # Traduire en arabe
    print("\n🇸🇦 Traduction en arabe...")
    translation_ar = TranslationService.translate_post(title, content, target_language='ar')
    print(f"  Titre: {translation_ar['title']}")
    print(f"  Contenu: {translation_ar['content']}")
    
    print("\n✅ Test de traduction terminé !")


def test_sentiment():
    """Test d'analyse de sentiment"""
    print("\n=== TEST D'ANALYSE DE SENTIMENT ===")
    
    texts = [
        "J'adore cette œuvre, elle est absolument magnifique !",
        "C'est vraiment décevant, je n'aime pas du tout.",
        "L'exposition présente différentes œuvres d'art contemporain.",
    ]
    
    for i, text in enumerate(texts, 1):
        print(f"\n📝 Texte {i}: {text}")
        result = SentimentModerationService.analyze_sentiment(text)
        
        emoji = {'positive': '😊', 'negative': '😔', 'neutral': '😐'}.get(result['label'], '📊')
        print(f"  {emoji} Sentiment: {result['label']}")
        print(f"  📊 Score: {result['score']:.2f}")
        print(f"  🎯 Confiance: {result['confidence']:.2f}")
        print(f"  💭 Explication: {result['explanation']}")
    
    print("\n✅ Test de sentiment terminé !")


def test_moderation():
    """Test de modération"""
    print("\n=== TEST DE MODÉRATION ===")
    
    contents = [
        "Magnifique exposition d'art contemporain, je recommande vivement !",
        "spam spam spam acheter maintenant !!!",  # Contenu spam
    ]
    
    for i, content in enumerate(contents, 1):
        print(f"\n📝 Contenu {i}: {content}")
        result = SentimentModerationService.moderate_content(content)
        
        status = "✅ Approprié" if result['is_appropriate'] else "❌ Inapproprié"
        print(f"  {status}")
        print(f"  🎯 Confiance: {result['confidence']:.2f}")
        
        if not result['is_appropriate']:
            print(f"  ⚠️ Raison: {result['reason']}")
            print(f"  📋 Catégories: {', '.join(result['categories'])}")
            print(f"  🔥 Sévérité: {result['severity']}")
    
    print("\n✅ Test de modération terminé !")


def test_full_post_processing():
    """Test du traitement complet d'un post"""
    print("\n=== TEST DE TRAITEMENT COMPLET ===")
    
    from blog.models import Post
    from django.contrib.auth.models import User
    
    # Créer un utilisateur de test si nécessaire
    user, created = User.objects.get_or_create(
        username='test_ai_user',
        defaults={'email': 'test@example.com'}
    )
    
    if created:
        user.set_password('testpass123')
        user.save()
        print("✅ Utilisateur de test créé")
    
    # Créer un post de test
    post = Post.objects.create(
        title="Test d'intégration IA",
        content="Ce post teste toutes les fonctionnalités IA : traduction, sentiment et modération.",
        author=user,
        original_language='fr'
    )
    
    print(f"\n📝 Post créé: {post.title}")
    print(f"   ID: {post.id}")
    
    # Traiter le post avec IA
    from blog.ai_services import process_post_with_ai
    
    print("\n🤖 Traitement IA en cours...")
    result = process_post_with_ai(post)
    
    print("\n📊 Résultats:")
    print(f"  😊 Sentiment: {result['sentiment']['label']} (score: {result['sentiment']['score']:.2f})")
    print(f"  ✅ Approprié: {result['moderation']['is_appropriate']}")
    print(f"  🌍 Traductions créées:")
    print(f"     - Anglais: {post.title_en}")
    print(f"     - Arabe: {post.title_ar}")
    print(f"     - Espagnol: {post.title_es}")
    
    print(f"\n✅ Test complet terminé ! (Post ID: {post.id})")
    print(f"   Vous pouvez voir ce post sur: http://127.0.0.1:8000/blog/post/{post.id}/")


def main():
    """Fonction principale"""
    print("=" * 60)
    print("🧪 TESTS DES FONCTIONNALITÉS IA DU BLOG")
    print("=" * 60)
    
    try:
        # Tests unitaires
        test_translation()
        test_sentiment()
        test_moderation()
        
        # Test d'intégration
        test_full_post_processing()
        
        print("\n" + "=" * 60)
        print("✅ TOUS LES TESTS SONT TERMINÉS !")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ ERREUR: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
