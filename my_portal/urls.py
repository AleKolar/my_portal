"""
URL configuration for my_portal project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect
from django.template.defaulttags import url

from django.urls import path, include

from news import views
from news.views import subscribe_news, subscribe_articles
from protect.views import IndexView
from sign.views import upgrade_me, BaseRegisterView, CustomLogoutView, update_profile

from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from news.views import Index

app_name = 'sign'



# Добавил немного последовательности, ТАК ЧТОБ открыл новость ИСПРАВИЛ - не понравилось. УДАЛИЛ, С РАСЧЕТОМ, ЧТО Я ПРАВИЛЬНО ПОНЯЛ ТЗ
urlpatterns = [
    path('admin/', admin.site.urls),

    path('news/', views.NewsListView.as_view(), name='news_list'),

    path('confirm_email/', upgrade_me, name='protect'),

    path('news/<int:id>/', views.news_full_detail, name='news_full_detail'),

    path('', include('sign.urls')),

    path('news/news_search/', views.PostsListView.as_view(), name='news_search'),

    path('news/create/', views.PostCreate.as_view(), name='create'),

    path('news/<int:pk>/edit/', views.PostUpdate.as_view()),

    path('edit/', views.PostUpdate.as_view()),

    path('', include('news.urls')),

    path('delete/', views.PostDelete.as_view(), name='delete'),

    path('<int:pk>/edit/', views.PostUpdate.as_view(), name='edit'),

    path('<int:pk>/delete/', views.PostUpdate.as_view(), name='delete'),


    path('accounts/login/protect/logout', LoginView.as_view(template_name='login.html', success_url='protect.html'),
            name='login'),

    path('login/',  LoginView.as_view(template_name='login.html', success_url='protect.html'),
            name='login'),

    path('login/', BaseRegisterView.as_view(template_name='signup.html'), name='signup'),

    path('login/protect/', include('news.urls')),

    path('login/protect/<int:pk>/edit', views.PostUpdate.as_view(), name='edit'),

    path('login/protect/<int:pk>/delete', views.PostUpdate.as_view(), name='delete'),

    path('login/protect/news/news_search', views.PostsListView.as_view(), name='news_search'),

    ########path('sign/logout/', CustomLogoutView.as_view()),

    path('accounts/', include('allauth.urls')), #####

    path('accounts/signup/protect/', IndexView.as_view()),

    path('accounts/signup/protect/news/', IndexView.as_view()),

    path('accounts/login/protect/', IndexView.as_view()),

    path('accounts/signup/protect/sign/logout/', CustomLogoutView.as_view()),

    path('accounts/signup/protect/news/', views.NewsListView.as_view()),

    path('accounts/email/news/', views.NewsListView.as_view()),

    path('accounts/email/profile', update_profile, name='profile.html'),

    path('accounts/signin/protect/news/', views.NewsListView.as_view()),

    path('accounts/signin/protect/profile', update_profile, name='profile.html'),

    path('accounts/signup/protect/upgrade', upgrade_me, name='upgrade'),

    path('accounts/logout/logout/', IndexView.as_view()),

    path('accounts/signup/', BaseRegisterView.as_view(template_name='signup.html'), name='signup'),


    path('accounts/signup/protect/logout', CustomLogoutView.as_view()),
    # ВОТ ЗДЕЕСЬ
    path('upgrade/', upgrade_me, name='protect'),


    ###path('', CustomLogoutView.as_view(), name='logout'),
    # not work 405 conflict post, get: path('protect/logout/', LogoutView.as_view(template_name='sign/logout.html'),
         #name='logout'),


    path('signup/', BaseRegisterView.as_view(template_name='signup.html'), name='signup'),

    path('login/protect/logout/', CustomLogoutView.as_view()),

    path('upgrade/protect/', upgrade_me, name='protect'),

    path('accounts/signup/', BaseRegisterView.as_view(template_name='signup.html'), name='signup'), # Автоматичесое добавл. в группу commom


    path('profile/', update_profile, name='profile.html'),

    path('confirm_email/', upgrade_me, name='protect'),
    path('confirm_email/sign/login/', include('protect.urls')),
    path('confirm_email/sign/login/sign/login/',include('protect.urls')),


    path('subscribe/news/', subscribe_news, name='subscribe_news'),
    path('subscribe/articles/', subscribe_articles, name='subscribe_articles'),


    # path('login/protect/news/<int:id>/', views.protect_news, name='protect_news'),
    # path('login/protect/articles/<int:id>/', views.protect_articles, name='protect_articles'),

    path('q_news/', views.q_news, name='q_news.html'),



    path('i18n/', include('django.conf.urls.i18n')),
    path('Index/', views.Index.as_view(), name='index_msg')


    ]

# urlpatterns += i18n_patterns(path('Index/', views.Index.as_view(), name='index_msg'),
#     path('', include('news.urls')), )



if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
