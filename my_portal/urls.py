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
from django.urls import path, include

from news import views

# НАСТРОИЛ, ТАК ЧТОБ ПО СТРАНИЦАМ ПЕРЕМЕЩАТЬСЯ ПОСЛЕДОВАТЕЛЬНО, С РАСЧЕТОМ, ЧТО Я ПРАВИЛЬНО ПОНЯЛ ТЗ
urlpatterns = [
    path('admin/', admin.site.urls),
    #path("news/", include("django.contrib.flatpages.urls")),

    path('news/<int:id>/', views.news_full_detail, name='news_full_detail'),

    path('news/news_search/', views.PostsListView.as_view(), name='news_search'),

    path('news/create/', views.PostCreate.as_view(), name='create'),

    path('news/<int:pk>/edit', views.PostUpdate.as_view()),


    path('', include('news.urls')),

    #path('', views.index, name='index'),

    path('edit/', views.PostUpdate.as_view(), name='edit'),

    ]
