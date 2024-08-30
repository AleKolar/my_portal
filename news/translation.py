from modeltranslation.translator import register, TranslationOptions
from .models import Post, Comment



@register(Post)
class MyPostTranslationOptions(TranslationOptions):
    fields = ('title', 'created_at', 'content', 'authorname')

@register(Comment)
class CommentTranslationOptions(TranslationOptions):
    fields = ('post', 'user', 'author', 'text', 'created_at', 'rating')
