from django.db import models
from django.contrib.auth.models import User
from artwork.models import Artwork  # Assurez-vous que cela correspond à l'emplacement de votre modèle Artwork

class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # L'utilisateur qui donne le feedback
    artwork = models.ForeignKey(Artwork, on_delete=models.CASCADE)  # L'œuvre concernée
    comment = models.TextField()  # Commentaire
    rating = models.PositiveSmallIntegerField()  # Note (par exemple, de 1 à 5)
    created_at = models.DateTimeField(auto_now_add=True)  # Date du feedback

    def __str__(self):
        return f"Feedback by {self.user.username} on {self.artwork.title}"

class Badge(models.Model):
    name = models.CharField(max_length=255)  # Nom du badge
    description = models.TextField()  # Description du badge
    criteria = models.PositiveIntegerField()  # Nombre de feedbacks requis pour obtenir le badge

    def __str__(self):
        return self.name
    @classmethod
    def create_initial_badges(cls):
        badges_data = [
            {"name": "Débutant", "description": "Attribué après 5 feedbacks", "criteria": 5},
            {"name": "Intermédiaire", "description": "Attribué après 10 feedbacks", "criteria": 10},
            {"name": "Avancé", "description": "Attribué après 15 feedbacks", "criteria": 15},
            {"name": "Expert", "description": "Attribué après 20 feedbacks", "criteria": 20},
            {"name": "Maître", "description": "Attribué après 50 feedbacks", "criteria": 50},
        ]

        for badge_data in badges_data:
            cls.objects.get_or_create(
                name=badge_data["name"],
                description=badge_data["description"],
                criteria=badge_data["criteria"]
            )
class UserBadge(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
    awarded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.badge.name}"
