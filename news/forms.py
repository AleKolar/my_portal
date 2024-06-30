from django import forms
from news.models import Post, Author


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'authorname', 'content']

    def __init__(self, *args, **kwargs):
        # user = kwargs.pop('user', None)
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['title'].label = "Название"
        self.fields['content'].label = "Текст публикации:"
        self.fields['authorname'].label = "Автор"

        # if user:
        #     author_instance, created = Author.objects.get_or_create(user=user)
        #     self.fields['author'].queryset = Author.objects.filter(user=user)
        # else:
        #     self.fields['author'].queryset = Author.objects.all()

    # ЗАКОМИТЕЛ, ТАК КАК В ЗАДАНИИ АВТОВЫБОР POST_TYPE
    #     self.post_type = Post.POST_TYPES
    #
    # def clean(self):
    #     if self.post_type not in ['news', 'article']:
    #         raise ValidationError("Invalid post_type value. It should be either 'news' or 'article'")





