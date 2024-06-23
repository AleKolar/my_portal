from django.template.defaulttags import url
from django.urls import path, include
from django.contrib.auth.views import LoginView

from sign.views import IndexView
from sign.views import BaseRegisterView, CustomLogoutView


urlpatterns = [

    path('',  LoginView.as_view(template_name='login.html', success_url='protect.html'),
         name='login'),

    #path('logout/', views.logout_user),
    # path('logout/', LogoutView.as_view(template_name='login.html'),
    #            name='logout'),


    path('sign/signup/', BaseRegisterView.as_view(template_name='signup.html'), name='signup'),

    path('protect/', IndexView.as_view()),

    path('sign/login/protect/sign/logout/', CustomLogoutView.as_view()),

    path('protect/', include('news.urls')),

    path('login/',  LoginView.as_view(template_name='login.html', success_url='protect.html'),
            name='login'),

    path('login/protect/', IndexView.as_view()),


    path('login/protect/sign/logout/', CustomLogoutView.as_view()),


    ]