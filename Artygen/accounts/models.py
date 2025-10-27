# accounts/models.py
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    ROLE_CHOICES = [
        ('user', 'User'),
        ('admin', 'Admin'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cin = models.CharField(max_length=20, null=True, blank=True)
    birthdate = models.DateField(null=True, blank=True)
    photo = models.ImageField(upload_to='', blank=True, null=True)  # Changé de 'profile_photos/' à '' pour éviter la duplication
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    
    # Nouveaux champs pour la bio IA
    bio = models.TextField(blank=True, null=True, help_text='Bio de profil')
    art_style = models.CharField(max_length=200, blank=True, null=True, help_text='Style artistique (ex: abstrait, réaliste, digital...)')
    art_interests = models.TextField(blank=True, null=True, help_text='Intérêts artistiques et mots-clés')
    bio_generated = models.BooleanField(default=False, help_text='La bio a été générée par IA')

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
