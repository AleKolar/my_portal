from django import forms
from .models import Profile


class ProfileForm(forms.ModelForm): # для п.1, там только rating, user_id , поэтому bio и pic
    class Meta:
        model = Profile
        fields = ['bio', 'profile_picture']