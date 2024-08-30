from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from .models import Author, Category, Post, PostCategory, Comment


class PostAdmin(admin.ModelAdmin):
    list_display = ('post_type', 'title', 'content', 'created_at', 'author', 'last_news')
    list_filter = ('created_at', 'post_type')
    search_fields = 'content', 'title'


class MyPostAdmin(TranslationAdmin): ###
    model = Post
class CommentAdmin(TranslationAdmin): ###
    model = Comment

admin.site.register(Post)
admin.site.register(Author)
admin.site.register(Category)
admin.site.register(PostCategory)
admin.site.register(Comment)
