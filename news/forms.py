from django import forms

from news.models import Post


class PostFilter(forms.ModelForm):
    class Meta:
        model = Post

        fields = {
            'title': ['icontains'],
            'authorname': ['icontains'],
            'created_at': ['gt'],

        }
