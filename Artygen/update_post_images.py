import os
import django

# Configuration de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'artify.settings')
django.setup()

from blog.models import Post

def update_post_images():
    """
    Corrige les chemins des images de posts qui contiennent 'profile_photos/'
    en enlevant ce préfixe pour éviter la duplication de chemin.
    """
    posts = Post.objects.filter(image__isnull=False).exclude(image='')
    updated_count = 0
    
    for post in posts:
        image_path = str(post.image)
        
        # Si le chemin contient 'profile_photos/', on l'enlève
        if image_path.startswith('profile_photos/'):
            new_path = image_path.replace('profile_photos/', '', 1)
            post.image = new_path
            post.save()
            updated_count += 1
            print(f"✓ Post '{post.title}': {image_path} → {new_path}")
        else:
            print(f"- Post '{post.title}': {image_path} (déjà correct)")
    
    print(f"\n✅ {updated_count} images de posts mises à jour!")
    print(f"📊 {posts.count()} posts vérifiés au total")

if __name__ == '__main__':
    print("🔄 Correction des chemins d'images de posts...\n")
    update_post_images()
