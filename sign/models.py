from news.models import Author
from django.db import models
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group


class Profile(models.Model):
    author = models.OneToOneField(Author, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)

    def __str__(self):
        return f'{self.author.user.username} Profile'


class BasicSignupForm(SignupForm): # Автоматическое добавление в common п.8

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        return user
