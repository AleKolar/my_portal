from django import forms

from news.models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post

        fields = [
            'title',
            'authorname',
            'created_at',

        ]
