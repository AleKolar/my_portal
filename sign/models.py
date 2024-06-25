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



class BasicSignupForm(SignupForm):
    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        user.email = self.cleaned_data['email']
        user.save()

        common_group, created = Group.objects.get_or_create(name='common')
        common_group.user_set.add(user)

        return user
