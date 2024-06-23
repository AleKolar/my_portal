from django.urls import path, include
from django.contrib.auth.views import LoginView

from protect.views import IndexView
from sign import views
from sign.views import BaseRegisterView, CustomLogoutView

urlpatterns = [

    path('',  LoginView.as_view(template_name='login.html', success_url='protect.html'),
         name='login'),
    #path('logout/', views.logout_user),
    # path('logout/', LogoutView.as_view(template_name='login.html'),
    #            name='logout'),

    path('signup/', BaseRegisterView.as_view(template_name='signup.html'),
         name='signup'),

    path('protect/', IndexView.as_view()),

    path('sign/protect/sign/logout/', CustomLogoutView.as_view()),

   ]