from allauth.account.models import EmailAddress
from allauth.account.views import email
from django.contrib.auth.models import User
from rest_framework import fields, serializers
from .models import Author, Post, Comment, Category


# class AuthorSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Author
#         fields = '__all__'


class CustomUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()  # Remove the 'source' keyword argument as it is redundant

    class Meta:
        model = User
        fields = ('username', 'email')


class AuthorSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()

    class Meta:
        model = Author
        fields = ('user', 'rating')


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.HyperlinkedRelatedField(view_name='user-detail', read_only=True)
    class Meta:
        model = Comment
        fields = ("post", "user", "author", "text", "created_at", "rating")


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ("name", "post_type")



