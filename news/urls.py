from django.urls import path
from . import views

# НАСТРОИЛ, ТАК ЧТОБ ПО СТРАНИЦАМ ПЕРЕМЕЩАТЬСЯ ПОСЛЕДОВАТЕЛЬНО, С РАСЧЕТОМ, ЧТО Я ПРАВИЛЬНО ПОНЯЛ ТЗ
urlpatterns = [

    path('news/', views.NewsListView.as_view(), name='news_list'),
    path('', views.index, name='index'),
    path('<int:pk>/delete', views.PostDelete.as_view(), name='delete'),
    path('news/<int:id>/', views.news_full_detail, name='news_full_detail'),
    path('<int:id>/', views.news_full_detail, name='news_full_detail'),
    path('news_search/', views.PostsListView.as_view(), name='news_search'),
    path('news/create/', views.PostCreate.as_view(), name='create'),
    path('news/<int:pk>/edit', views.PostUpdate.as_view(), name='edit'),
    path('news/<int:pk>/delete/', views.PostDelete.as_view(), name='delete'),



    path('articles/', views.ArticlesListView.as_view(), name='articles_list'),

    path('articles/create/', views.PostCreate.as_view(), name='create'),

    path('articles/<int:id>/', views.articles_full_detail, name='articles_full_detail'), # all art

    path('articles/<int:pk>/edit', views.PostUpdate.as_view(), name='edit'),

    path('articles/<int:pk>/delete/', views.PostDelete.as_view(), name='delete'),

]




