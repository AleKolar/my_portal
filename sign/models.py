from django.contrib.auth.decorators import login_required, permission_required
from news.models import Author, Post
from django.db import models
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType



class BasicSignupForm(SignupForm):
    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        user.email = self.cleaned_data['email']
        user.save()
        common_group, created = Group.objects.get_or_create(name='common')
        common_group.user_set.add(user)
        return user


class Profile(models.Model):
    author = models.OneToOneField(Author, on_delete=models.CASCADE, blank=True)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    def __str__(self):
        return f'{self.author.user.username} Profile'


# п. 10 предоставить права создания и редактирования. в django admin есть: can add post, can delete post, can view
# Но все равно, это же надо было делать?
class Meta:
    permissions = [
        ("create_post", "Can create a post"),
        ("edit_post", "Can edit a post"),
    ]

    @login_required
    @permission_required('auth.add_user')
    def assign_permissions(self):
        authors_group = Group.objects.get(name='authors')
        content_type = ContentType.objects.get_for_model(Post)
        #authors_group, created = Group.objects.get_or_create(name='authors')

        create_post_permission = Permission.objects.get(content_type=content_type, codename='create_post')
        edit_post_permission = Permission.objects.get(content_type=content_type, codename='edit_post')

        authors_group.permissions.add(create_post_permission, edit_post_permission)
