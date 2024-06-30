from django import forms
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.shortcuts import render, redirect, get_object_or_404

from news.forms import PostForm
from news.models import Author, Post
from sign.form import ProfileForm
from sign.models import Profile, BasicSignupForm


# Для п.9 Создать возможность стать автором (быть добавленным в группу authors)
class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'protect.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        return context



@login_required
def upgrade_me(request):
    if request.method == 'POST':
        authors_group, created = Group.objects.get_or_create(name='authors')
        if not request.user.groups.filter(name='authors').exists():
            request.user.groups.add(authors_group)
            messages.success(request, 'Вы добавлены в группу authors!')

            user_id = request.user.id
            author, created = Author.objects.get_or_create(user_id=user_id)

            posts = Post.objects.filter(author=None)
            posts.update(author=author)

            user_name = request.user.username

        else:
            messages.info(request, 'Вы уже в группе authors.')
        print("Messages added:", messages.get_messages(request))  # Это мне проверку посоветовали, чтоб отслеживать
        return redirect('/')
    else:
        return redirect('/')


class BaseRegisterForm(UserCreationForm):
    email = forms.EmailField(label="Email")
    first_name = forms.CharField(label="Имя")
    last_name = forms.CharField(label="Фамилия")


class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/'

    class Meta:
        model = User
        fields = ("username",
                  "first_name",
                  "last_name",
                  "email",
                  "password1",
                  "password2",)


# ФУНКЦИЯ ВЫХОДА
class CustomLogoutView(TemplateView):
    template_name = 'logout.html'

    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)
        # return redirect('logout')


def profile_view(request):  # Для выхода из Редактора профиля
    return render(request, 'logout.html')


# п. 1 ЭТО РЕДАКТИРОВАНИЕ ПРОФИЛЯ
@login_required  # 1. В классе-представлении редактирования профиля добавить проверку аутентификации.
def update_profile(request):
    try:
        author = request.user.author
    except Author.DoesNotExist:
        author = Author.objects.create(user=request.user)

    from sign.models import Profile
    try:
        profile = author.profile
    except Profile.DoesNotExist:
        profile = Profile.objects.create(author=author)

    if request.method == 'POST':
        user_form = UserChangeForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('protect')
    else:
        user_form = UserChangeForm(instance=request.user)
        profile_form = ProfileForm(instance=profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }

    return render(request, 'profile.html', context)