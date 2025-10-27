from django import forms
from .models import Event
from django.contrib.auth.models import User

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'location', 'date', 'capacity', 'image', 'event_type']  # Update this field name


class InviteParticipantsForm(forms.Form):
    participants = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Invite Users"
    )
class ParticipantForm(forms.Form):
    email = forms.EmailField(label='Participant Email', max_length=254)
