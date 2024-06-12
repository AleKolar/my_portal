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


urlpatterns = [
    path('admin/', admin.site.urls),
    #path("news/", include("django.contrib.flatpages.urls")),
    path('', include('news.urls')), # для 1, 2
    #path('/<int:id>/', views.news_full_detail, name='news_full_detail'), # для 3
    #path('news/news_full_detail', views.news_full_detail, name='news_full_detail'),
    path('int:id/', views.news_full_detail, name='news_full_detail'),
]
