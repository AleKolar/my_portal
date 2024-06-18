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
            'author',

        ]

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['authorname'].label = "Автор"
        self.fields['title'].label = "Название"
        self.fields['content'].label = "Текст публикации:"
        self.fields['author'].label = "id"

    # ЗАКОМИТЕЛ, ТАК КАК В ЗАДАНИИ АВТОВЫБОР POST_TYPE
    #     self.post_type = Post.POST_TYPES
    #
    # def clean(self):
    #     if self.post_type not in ['news', 'article']:
    #         raise ValidationError("Invalid post_type value. It should be either 'news' or 'article'")





