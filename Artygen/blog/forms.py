from django import forms
from .models import Favourites

class FavouriteNoteForm(forms.ModelForm):
    note = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False)
    priority = forms.ChoiceField(choices=[('High', 'Haute'), ('Medium', 'Moyenne'), ('Low', 'Basse')], required=True)

    class Meta:
        model = Favourites
        fields = ['note', 'priority']
