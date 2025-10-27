# gallery/forms.py
from django import forms
from .models import Gallery

class GalleryForm(forms.ModelForm):
    class Meta:
        model = Gallery
        fields = ['name', 'owner', 'location', 'theme', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Gallery Name'}),
            'location': forms.TextInput(attrs={'placeholder': 'Location'}),
            'theme': forms.TextInput(attrs={'placeholder': 'Theme'}),
            'description': forms.Textarea(attrs={'placeholder': 'Description'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        # Additional custom validations can be added here if necessary
