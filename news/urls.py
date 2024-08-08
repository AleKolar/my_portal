from . import views
### from django.views.decorators.cache import cache_page
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    #####CASHES#### path('news/', cache_page(60)(views.NewsListView.as_view()), name='news_list'),
    path('news/', views.NewsListView.as_view(), name='news_list'),
    # path('', views.index, name='index'),
    path('<int:pk>/delete', views.PostDelete.as_view(), name='delete'),
    path('news/<int:id>/', views.news_full_detail, name='news_full_detail'),
    path('<int:id>/', views.news_full_detail, name='news_full_detail'),
    path('news_search/', views.PostsListView.as_view(), name='news_search'),
    path('news/create/', views.PostCreate.as_view(), name='create'),
    path('news/<int:pk>/edit', views.PostUpdate.as_view(), name='edit'),
    path('news/<int:pk>/delete/', views.PostDelete.as_view(), name='delete'),

    #####CASHES#### path('articles/', cache_page(60)(views.ArticlesListView.as_view()), name='articles_list'),
    path('articles/', views.ArticlesListView.as_view(), name='articles_list'),

    path('articles/create/', views.PostCreate.as_view(), name='create'),

    path('articles/<int:id>/', views.articles_full_detail, name='articles_full_detail'),  # all art

    path('articles/<int:pk>/edit', views.PostUpdate.as_view(), name='edit'),

    path('articles/<int:pk>/delete/', views.PostDelete.as_view(), name='delete'),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)