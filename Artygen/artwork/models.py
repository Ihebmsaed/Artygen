from django.db import models
from django.contrib.auth.models import User  # Importer le modèle User
from category.models import Category  # Importer le modèle Category

class Artwork(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  # ForeignKey vers Category
    file = models.FileField(upload_to='artworks/files/')
    tags = models.CharField(max_length=255, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)  # Rendre le champ nullable

    def __str__(self):
        return self.title
    

class ArtCollection(models.Model):
    name = models.CharField(max_length=255)
    artworks = models.ManyToManyField(Artwork, related_name='collections')  # Relation plusieurs-à-plusieurs avec Artwork
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)  # Optionnel: utilisateur qui a créé la collection

    def __str__(self):
        return self.name