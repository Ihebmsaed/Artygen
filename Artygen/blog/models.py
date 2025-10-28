from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    liked_by = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    likes_count = models.PositiveIntegerField(default=0)  # Champ pour stocker le nombre de likes
    image = models.ImageField(upload_to='', blank=True, null=True)  # Ajout du champ image
    
    # Champs pour l'analyse de sentiment et la modération
    sentiment_score = models.FloatField(null=True, blank=True)  # Score de -1 (négatif) à 1 (positif)
    sentiment_label = models.CharField(max_length=20, null=True, blank=True)  # positive, negative, neutral
    is_appropriate = models.BooleanField(default=True)  # False si contenu inapproprié détecté
    moderation_reason = models.TextField(null=True, blank=True)  # Raison si modéré
    moderation_date = models.DateTimeField(null=True, blank=True)
    
    # Champs pour les traductions
    title_en = models.CharField(max_length=200, null=True, blank=True)
    content_en = models.TextField(null=True, blank=True)
    title_fr = models.CharField(max_length=200, null=True, blank=True)
    content_fr = models.TextField(null=True, blank=True)
    title_ar = models.CharField(max_length=200, null=True, blank=True)
    content_ar = models.TextField(null=True, blank=True)
    title_es = models.CharField(max_length=200, null=True, blank=True)
    content_es = models.TextField(null=True, blank=True)
    original_language = models.CharField(max_length=10, default='fr')  # Langue d'origine

    

    def __str__(self):
        return self.title
    @property
    def author_profile_photo(self):
        return self.author.profile.photo.url if self.author.profile.photo else None


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    
    # Champs pour l'analyse de sentiment et la modération
    sentiment_score = models.FloatField(null=True, blank=True)
    sentiment_label = models.CharField(max_length=20, null=True, blank=True)
    is_appropriate = models.BooleanField(default=True)
    moderation_reason = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.author.username} comment on {self.post.title}'
    @property
    def author_profile_photo(self):
        return self.author.profile.photo.url if self.author.profile.photo else None

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    is_like = models.BooleanField()  #True pour un like, False pour un dislike

    class Meta:
        unique_together = ('user', 'post')


class Favourites(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    added_on = models.DateTimeField(default=timezone.now)  # Date d'ajout du favori
    priority = models.CharField(max_length=10, choices=[('High', 'Haute'), ('Medium', 'Moyenne'), ('Low', 'Basse')], default='Medium')
    note = models.TextField()

    def __str__(self):
        return f"Favourites: {self.post.title} by {self.user.username}"