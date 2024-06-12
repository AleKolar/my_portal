from django.urls import path
from . import views


urlpatterns = [
    # ЭТО ВСЕ МНЕ НУЖНО ДЛЯ ВИЗУАЛИЗАЦИИ И ЗАКРЕПЛЕНИЯ МАТЕРИАЛА
    #path('news_full_detail/<int:id>', views.news_full_detail, name='news_full_detail'),
    path('news/', views.NewsListView.as_view(), name='news_list'),
    #path('news/<int:pk>/', views.NewsDetailView.as_view(), name='news_detail'),
    #path('article', views.PostsListView.as_view(), name='article_list'),
    #path('article/<int:pk>', views.PostsDetailView.as_view(), name='article_detail'),
    #path('news/<int:id>/', views.news_full_detail, name='news_full_detail'),
    #path('news/<int:pk>/', views.NewsDetailView.as_view(), name='news_detail'),
    path('', views.index, name='index'),
    path('<int:id>/', views.news_full_detail, name='news_full_detail'),

    path('<int:id>/', views.NewsDetailView.as_view(), name='news_full_detail'),
]




