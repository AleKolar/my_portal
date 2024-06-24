from django import forms
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.shortcuts import render, redirect


from news.models import Author
from sign.form import ProfileForm


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'protect.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        return context

# @login_required
# def upgrade_me(request):
#     user = request.user
#     authors_group = Group.objects.get(name='authors')
#     is_not_author = not request.user.groups.filter(name='authors').exists()
#
#     if request.method == 'POST' and is_not_author:
#         authors_group.user_set.add(user)
#         return redirect('/')
#
#     return render(request, 'protect.html', {'is_not_author': is_not_author})


@login_required
def upgrade_me(request):
    if request.method == 'POST':
        authors_group, created = Group.objects.get_or_create(name='authors')
        if not request.user.groups.filter(name='authors').exists():
            request.user.groups.add(authors_group)
            messages.success(request, 'Вы добавлены в группу authors!')
        else:
            messages.info(request, 'Вы уже в группе authors.')
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
                  "password2", )


class CustomLogoutView(TemplateView):
    template_name = 'logout.html'

    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)


def profile_view(request): # Для выхода из Редактора профиля
    return render(request, 'logout.html')





@login_required # 1. В классе-представлении редактирования профиля добавить проверку аутентификации.
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
            return redirect('profile')
    else:
        user_form = UserChangeForm(instance=request.user)
        profile_form = ProfileForm(instance=profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }

    return render(request, 'profile.html', context)
