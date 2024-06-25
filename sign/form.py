from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm): # для п.1
    class Meta:
        model = Profile
        fields = ['bio', 'profile_picture']
