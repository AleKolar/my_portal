from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)


    def update_rating(self):
        post_rating = sum([post.rating * 3 for post in self.post_set.all()])
        comment_rating = sum([comment.rating for comment in Comment.objects.filter(author=self)])
        post_comment_rating = sum([comment.rating for comment in Comment.objects.filter(post__author=self)])

        self.rating = post_rating + comment_rating + post_comment_rating
        self.save()

    def __str__(self):
        return self.user.username

    # Как-то не пришлось ей воспользоваться
    def best_user(self):
        best_author = Author.objects.all().order_by('-rating').first()
        best_user = best_author.user
        return best_user.user, best_author.rating



class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    post_type = models.CharField(max_length=255, choices=[('news', 'News'), ('article', 'Article')])
    subscribers = models.ManyToManyField(User, related_name='subscribed_categories', blank=True)

    def subscribe_user(self, user):
        try:
            existing_category = Category.objects.get(pk=self.pk)
            existing_category.subscribers.add(user)
        except ObjectDoesNotExist:
            raise "категории еще нет"

class Post(models.Model):
    author = models.ForeignKey('Author', on_delete=models.CASCADE)
    POST_TYPES = (
        ('article', 'Article'),
        ('news', 'News'),    )

    post_type = models.CharField(max_length=10, choices=POST_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField('Category', through='PostCategory')
    title = models.CharField(max_length=255)
    content = models.TextField()
    rating = models.IntegerField(default=0)
    authorname = models.CharField(max_length=255,)



    def __str__(self):
        return f'{self.authorname}: {self.content[:21]}'

    def get_absolute_url(self):
        if self.post_type  == 'news':
            return reverse('news_full_detail', args=[str(self.id)])
        else:
            return reverse('articles_full_detail', args=[str(self.id)])

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.content[:124] + '... something important'

    def display_best_post(self):
        best_post = Post.objects.filter(categories__name='Category1').order_by('-rating').first()
        best_post_preview = best_post.preview()
        best_post_content = best_post.content[:50]
        print("Best Post:")
        print("Created at:", best_post.created_at)
        print("Author:", best_post.author.user.username)
        print("Rating:", best_post.rating)
        print("Title:", best_post.title)
        print("Preview:", best_post_preview)
        print("Сontent:", best_post_content)
        return best_post


class PostCategory(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)


    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()


