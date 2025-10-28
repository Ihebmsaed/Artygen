"""
Script de vérification et de test du système de gestion de blog avec IA
Ce script vérifie :
1. Les migrations de la base de données
2. Les configurations des services IA
3. Les URLs et les vues
4. Les templates
"""

import os
import sys
import django

# Configuration de Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'artify.settings')
django.setup()

from django.core.management import call_command
from blog.models import Post, Comment
from blog.ai_services import TranslationService, SentimentModerationService
from django.contrib.auth.models import User
from django.conf import settings

def check_database_migrations():
    """Vérifie que toutes les migrations sont appliquées"""
    print("\n" + "="*60)
    print("1. VÉRIFICATION DES MIGRATIONS")
    print("="*60)
    
    try:
        # Vérifier si les champs existent dans le modèle Post
        post_fields = [f.name for f in Post._meta.get_fields()]
        
        required_fields = [
            'sentiment_score', 'sentiment_label', 'is_appropriate',
            'moderation_reason', 'moderation_date', 'original_language',
            'title_en', 'title_fr', 'title_ar', 'title_es',
            'content_en', 'content_fr', 'content_ar', 'content_es'
        ]
        
        missing_fields = [field for field in required_fields if field not in post_fields]
        
        if missing_fields:
            print(f"❌ Champs manquants dans Post: {missing_fields}")
            print("   Exécutez: python manage.py makemigrations blog")
            print("   Puis: python manage.py migrate blog")
            return False
        else:
            print("✅ Tous les champs du modèle Post sont présents")
        
        # Vérifier les champs de Comment
        comment_fields = [f.name for f in Comment._meta.get_fields()]
        required_comment_fields = [
            'sentiment_score', 'sentiment_label', 'is_appropriate',
            'moderation_reason'
        ]
        
        missing_comment_fields = [field for field in required_comment_fields if field not in comment_fields]
        
        if missing_comment_fields:
            print(f"❌ Champs manquants dans Comment: {missing_comment_fields}")
            return False
        else:
            print("✅ Tous les champs du modèle Comment sont présents")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la vérification des migrations: {e}")
        return False

def check_ai_services():
    """Vérifie que les services IA sont configurés"""
    print("\n" + "="*60)
    print("2. VÉRIFICATION DES SERVICES IA")
    print("="*60)
    
    # Vérifier la clé API
    try:
        api_key = os.getenv("API_KEY") or getattr(settings, 'GEMINI_API_KEY', None)
        if api_key:
            print(f"✅ Clé API Gemini configurée: {api_key[:10]}...")
        else:
            print("❌ Clé API Gemini non configurée")
            print("   Ajoutez GEMINI_API_KEY dans settings.py ou API_KEY dans .env")
            return False
    except Exception as e:
        print(f"❌ Erreur lors de la vérification de la clé API: {e}")
        return False
    
    # Test simple de traduction (sans appel API réel)
    try:
        print("✅ Service de traduction importé avec succès")
        print("✅ Service d'analyse de sentiment importé avec succès")
        return True
    except Exception as e:
        print(f"❌ Erreur lors de l'import des services: {e}")
        return False

def check_urls():
    """Vérifie que toutes les URLs sont configurées"""
    print("\n" + "="*60)
    print("3. VÉRIFICATION DES URLS")
    print("="*60)
    
    from django.urls import reverse, NoReverseMatch
    
    urls_to_check = [
        'post-home',
        'post-Create',
        'user-posts',
        'favourites',
        'moderation-dashboard',
    ]
    
    all_ok = True
    for url_name in urls_to_check:
        try:
            url = reverse(url_name)
            print(f"✅ URL '{url_name}': {url}")
        except NoReverseMatch:
            print(f"❌ URL '{url_name}' non trouvée")
            all_ok = False
    
    return all_ok

def check_templates():
    """Vérifie que les templates existent"""
    print("\n" + "="*60)
    print("4. VÉRIFICATION DES TEMPLATES")
    print("="*60)
    
    from django.template.loader import get_template
    from django.template import TemplateDoesNotExist
    
    templates_to_check = [
        'Blog/blog.html',
        'Blog/detail_Blog.html',
        'Blog/create.html',
        'Blog/user_posts.html',
        'Blog/moderation_dashboard.html',
    ]
    
    all_ok = True
    for template_name in templates_to_check:
        try:
            get_template(template_name)
            print(f"✅ Template '{template_name}' trouvé")
        except TemplateDoesNotExist:
            print(f"❌ Template '{template_name}' non trouvé")
            all_ok = False
    
    return all_ok

def check_static_files():
    """Vérifie que les fichiers statiques existent"""
    print("\n" + "="*60)
    print("5. VÉRIFICATION DES FICHIERS STATIQUES")
    print("="*60)
    
    import os
    base_dir = settings.BASE_DIR
    
    static_files = [
        'static/js/blog-ai-features.js',
        'static/css/custom-forms.css',
    ]
    
    all_ok = True
    for file_path in static_files:
        full_path = os.path.join(base_dir, file_path)
        if os.path.exists(full_path):
            print(f"✅ Fichier '{file_path}' trouvé")
        else:
            print(f"⚠️  Fichier '{file_path}' non trouvé (peut être optionnel)")
    
    return all_ok

def run_database_test():
    """Test rapide de la base de données"""
    print("\n" + "="*60)
    print("6. TEST DE LA BASE DE DONNÉES")
    print("="*60)
    
    try:
        # Compter les posts
        post_count = Post.objects.count()
        print(f"✅ Nombre de posts: {post_count}")
        
        # Compter les commentaires
        comment_count = Comment.objects.count()
        print(f"✅ Nombre de commentaires: {comment_count}")
        
        # Compter les utilisateurs
        user_count = User.objects.count()
        print(f"✅ Nombre d'utilisateurs: {user_count}")
        
        # Vérifier les posts avec sentiment
        posts_with_sentiment = Post.objects.filter(sentiment_label__isnull=False).count()
        print(f"✅ Posts avec analyse de sentiment: {posts_with_sentiment}")
        
        # Vérifier les posts flaggés
        flagged_posts = Post.objects.filter(is_appropriate=False).count()
        print(f"✅ Posts flaggés pour modération: {flagged_posts}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test de la base de données: {e}")
        return False

def main():
    """Fonction principale"""
    print("\n" + "="*60)
    print("VÉRIFICATION DU SYSTÈME DE GESTION DE BLOG")
    print("="*60)
    
    results = []
    
    results.append(("Migrations", check_database_migrations()))
    results.append(("Services IA", check_ai_services()))
    results.append(("URLs", check_urls()))
    results.append(("Templates", check_templates()))
    results.append(("Fichiers statiques", check_static_files()))
    results.append(("Base de données", run_database_test()))
    
    print("\n" + "="*60)
    print("RÉSUMÉ")
    print("="*60)
    
    for name, status in results:
        status_icon = "✅" if status else "❌"
        print(f"{status_icon} {name}")
    
    all_ok = all(status for _, status in results)
    
    if all_ok:
        print("\n✅ TOUS LES TESTS SONT PASSÉS!")
        print("Le système de gestion de blog est opérationnel.")
    else:
        print("\n⚠️  CERTAINS TESTS ONT ÉCHOUÉ")
        print("Veuillez corriger les erreurs ci-dessus.")
    
    print("\n" + "="*60)
    print("ACTIONS RECOMMANDÉES:")
    print("="*60)
    print("1. Si des migrations sont manquantes:")
    print("   python manage.py makemigrations blog")
    print("   python manage.py migrate")
    print("\n2. Pour appliquer les migrations existantes:")
    print("   python manage.py migrate")
    print("\n3. Pour créer un superutilisateur (admin):")
    print("   python manage.py createsuperuser")
    print("\n4. Pour lancer le serveur:")
    print("   python manage.py runserver")
    print("\n5. Pour accéder au dashboard de modération:")
    print("   http://127.0.0.1:8000/blog/moderation/")
    print("="*60)

if __name__ == "__main__":
    main()
