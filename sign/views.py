from django.contrib.auth import logout
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm
from django.shortcuts import render, redirect
from .models import BaseRegisterForm


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'protect.html'


# def logout_user(request):
#     logout(request)
#     return HttpResponseRedirect(reverse('login'))


class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/'


class CustomLogoutView(TemplateView):
    template_name = 'logout.html'

    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView
from .models import User

class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = User
    fields = ['username', 'password1', 'password2']
    template_name = 'profile_edit.html'

    def get_object(self, queryset=None):
        return self.request.user.profile



def profile_edit(request):
    if request.method == 'POST':
        user_form = UserChangeForm(request.POST, instance=request.user)
        profile_form = BaseRegisterForm(request.POST, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')

    else:
        user_form = UserChangeForm(instance=request.user)
        profile_form = BaseRegisterForm(instance=request.user.profile)

    return render(request, 'profile_edit.html', {'user_form': user_form, 'profile_form': profile_form})
