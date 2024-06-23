
from django.contrib.auth import logout, login
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView
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
