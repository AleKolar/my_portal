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
from django.contrib.auth.views import LogoutView, LoginView
from django.urls import path, include

import sign
from news import views
from protect.views import IndexView
from sign.views import BaseRegisterView, CustomLogoutView

# Добавил немного последовательности, ТАК ЧТОБ открыл новость ИСПРАВИЛ - не понравилось. УДАЛИЛ, С РАСЧЕТОМ, ЧТО Я ПРАВИЛЬНО ПОНЯЛ ТЗ
urlpatterns = [
    path('admin/', admin.site.urls),

    path('news/<int:id>/', views.news_full_detail, name='news_full_detail'),

    path('news/news_search/', views.PostsListView.as_view(), name='news_search'),

    path('news/create/', views.PostCreate.as_view(), name='create'),

    path('news/<int:pk>/edit', views.PostUpdate.as_view()),

    path('', include('news.urls')),

    path('edit/', views.PostUpdate.as_view(), name='edit'),

    path('delete/', views.PostDelete.as_view(), name='delete'),

    path('<int:pk>/edit', views.PostUpdate.as_view(), name='edit'),

    path('<int:pk>/delete', views.PostUpdate.as_view(), name='delete'),     


    path('', include('sign.urls')),

    path('login/protect/', include('news.urls')),

    path('login/protect/<int:pk>/edit', views.PostUpdate.as_view(), name='edit'),

    path('login/protect/<int:pk>/delete', views.PostUpdate.as_view(), name='delete'),

    path('login/protect/news/news_search', views.PostsListView.as_view(), name='news_search'),


    path('accounts/', include('allauth.urls')),

    path('accounts/logout/logout/', CustomLogoutView.as_view()),

    path('accounts/signup/protect/', IndexView.as_view()),

    path('accounts/login/protect/', IndexView.as_view())




    ]


