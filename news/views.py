from .models import Post
from django.shortcuts import render
from django.views.generic import ListView, DetailView

def index(request):
    return render(request, 'index.html')

def news_full_detail(request, id):
    post = Post.objects.get(pk=id)
    post_info = {
        'title': post.title,
        'content': post.content,
        'publish_date': post.created_at.strftime('%d.%m.%Y'),
        'author': post.author,
    }
    return render(request, 'news_full_detail.html', {'post': post_info})


# def news_list(request):
#     news = Post.objects.filter(post_type='news').order_by('-created_at')
#     return render(request, 'news_list.html', {'news': news})

# def news_full_detail(request):
#     posts = Post.objects.order_by('-created_at')
#     posts_info = []
#     for post in posts:
#         post_info = {
#             'title': post.title,
#             'publish_date': post.created_at,
#             'content_excerpt': post.content[:20]
#         }
#         posts_info.append(post_info)
#     return render(request, 'news_full_detail.html', {'news_posts': posts_info})

class NewsListView(ListView):
    model = Post
    template_name = 'news_list.html'
    queryset = Post.objects.filter(post_type='news').order_by('-created_at')[:21]
    context_object_name = 'news'

class NewsDetailView(DetailView):
    model = Post
    template_name = 'news_detail.html'
    context_object_name = 'news'


class PostsListView(ListView):
    model = Post
    template_name = 'article_list.html'
    queryset = Post.objects.filter(post_type='article').order_by('-created_at')[:20]
    context_object_name = 'article'

class PostsDetailView(DetailView):
    model = Post
    template_name = 'article_detail.html'
    context_object_name = 'article'
