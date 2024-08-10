from django import forms
from news.models import Post, Author, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'authorname', 'content', 'id']

    def __init__(self, *args, **kwargs):
        # user = kwargs.pop('user', None)
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['title'].label = "Название"
        self.fields['content'].label = "Текст публикации:"
        self.fields['authorname'].label = "Автор"

class CommentForm(forms.ModelForm):
    ### author = forms.CharField(max_length=100, label='Author')  # Add author field
    text = forms.CharField(widget=forms.Textarea(attrs={'rows': 4, 'cols': 50}), label='Comment Text')  # Add text field
    class Meta:
        model = Comment
        fields = ['author', 'text']
        labels = {'text': 'Comment Text'}
        widgets = {
            'text': forms.Textarea(attrs={'rows': 4, 'cols': 50})  # Customize the size of the text area
        }





