from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class CustomUserCreationForm(UserCreationForm):
    ROLE_CHOICES = [
        ('user', 'User'),
        ('admin', 'Admin'),
    ]

    first_name = forms.CharField(max_length=30, required=True, help_text='First Name')
    last_name = forms.CharField(max_length=30, required=True, help_text='Last Name')
    email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')
    cin = forms.CharField(max_length=20, required=True, help_text='CIN')
    birthdate = forms.DateField(required=True, widget=forms.DateInput(attrs={'type': 'date'}), help_text='Birthdate')
    profile_image = forms.ImageField(required=False, help_text='📷 Upload your profile picture (optional).')
    role = forms.ChoiceField(choices=ROLE_CHOICES, required=True, help_text='Select User Role')
    
    # New fields for AI bio generation
    art_style = forms.CharField(
        max_length=200, 
        required=False,
        help_text='🎨 Your artistic style (ex: Abstract, Realistic, Digital Art, Photography...)',
        widget=forms.TextInput(attrs={'placeholder': 'Ex: Abstract painting, futuristic digital art...'})
    )
    art_interests = forms.CharField(
        required=False,
        help_text='🌟 Your artistic interests and keywords (separated by commas)',
        widget=forms.Textarea(attrs={
            'placeholder': 'Ex: nature, portraits, bright colors, emotions, surrealism, architecture...',
            'rows': 3
        })
    )
    generate_bio = forms.BooleanField(
        required=False,
        initial=True,
        help_text='✨ Automatically generate my profile bio with AI',
        widget=forms.CheckboxInput()
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'cin', 'birthdate', 'profile_image', 'role', 'art_style', 'art_interests', 'generate_bio')
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Username'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
            'password1': forms.PasswordInput(attrs={'placeholder': 'Password'}),
            'password2': forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}),
            'cin': forms.TextInput(attrs={'placeholder': 'CIN'}),
            'birthdate': forms.DateInput(attrs={'type': 'date', 'placeholder': 'Birthdate'}),
            'profile_image': forms.ClearableFileInput(attrs={'placeholder': 'Profile Picture'}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        
        # Grant admin access if the role is admin
        if self.cleaned_data['role'] == 'admin':
            user.is_staff = True
            user.is_superuser = True  # This grants full access to the admin interface

        if commit:
            user.save()
            
            # Get or create the profile (created automatically by the signal)
            profile = user.profile
            
            # Update profile fields
            profile.cin = self.cleaned_data['cin']
            profile.birthdate = self.cleaned_data['birthdate']
            profile.role = self.cleaned_data['role']
            profile.art_style = self.cleaned_data.get('art_style', '')
            profile.art_interests = self.cleaned_data.get('art_interests', '')
            
            # Handle photo separately (IMPORTANT for files)
            profile_image = self.cleaned_data.get('profile_image')
            if profile_image:
                profile.photo = profile_image
            
            profile.save()
        return user
