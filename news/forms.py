from django import forms

from news.models import Post

from django.core.exceptions import ValidationError

class PostForm(forms.ModelForm):
    class Meta:
        model = Post

        fields = [
            'title',
            'authorname',
            'content',
            'author'
        ]

        # def clean(self):
        #     cleaned_data = super().clean()
        #     description = cleaned_data.get("content")
        #     if description is not None and len(description) < 20:
        #         raise ValidationError({
        #             "content": "Текст публикации не может быть менее 20 символов."
        #         })
        #
        #     return cleaned_data

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['authorname'].label = "Автор"
        self.fields['title'].label = "Название"
        self.fields['content'].label = "Текст публикации:"
        self.fields['author'].label = "id"

