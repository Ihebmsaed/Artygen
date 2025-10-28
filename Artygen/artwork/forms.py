from django import forms
from .models import Artwork
from .models import ArtCollection

class ArtworkForm(forms.ModelForm):
    class Meta:
        model = Artwork
        fields = ['title', 'description', 'category', 'file', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Artwork Title'}),
 'description': forms.Textarea(attrs={
                'class': 'form-control', 
                'placeholder': 'Artwork Description',
                'rows': 3,  # Reduced height (number of lines)
                'cols': 50  # Optional width (you can adjust or remove this attribute)
            }),            'category': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Artwork Category'}),

            'file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'tags': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tags'}),
        }

class ArtCollectionForm(forms.ModelForm):
    class Meta:
        model = ArtCollection
        fields = ['name']  