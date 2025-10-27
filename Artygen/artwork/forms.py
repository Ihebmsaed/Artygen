from django import forms
from .models import Artwork
from .models import ArtCollection

class ArtworkForm(forms.ModelForm):
    class Meta:
        model = Artwork
        fields = ['title', 'description', 'category', 'file', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Titre de l\'œuvre'}),
 'description': forms.Textarea(attrs={
                'class': 'form-control', 
                'placeholder': 'Description de l\'œuvre',
                'rows': 3,  # Réduit la hauteur (nombre de lignes)
                'cols': 50  # Largeur optionnelle (tu peux ajuster ou supprimer cet attribut)
            }),            'category': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Categorie de l\'œuvre'}),

            'file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'tags': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tags'}),
        }
class ArtCollectionForm(forms.ModelForm):
    class Meta:
        model = ArtCollection
        fields = ['name']  # Si vous avez d'autres champs, ajoutez-les ici