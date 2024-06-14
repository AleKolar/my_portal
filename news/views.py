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

class NewsListView(ListView):
    model = Post
    template_name = 'news_list.html'
    #ordering = ['title', 'author', '-created_at'] # разбираюсь с постраничным выводом
    #queryset = Post.objects.filter(post_type='news').order_by('-created_at')
    queryset = Post.objects.all().order_by('-created_at') # разбираюсь с постраничным выводом
    context_object_name = 'news' # разбираюсь с постраничным выводом
    paginate_by = 4# разбираюсь с постраничным выводом

class NewsDetailView(DetailView):
    model = Post
    template_name = 'news_full_detail.html'
    context_object_name = 'news'


class PostsListView(ListView):
    model = Post
    template_name = 'article_list.html'
    #queryset = Post.objects.filter(post_type='article').order_by('-created_at')[:20]
    queryset = Post.objects.all().order_by('-created_at')[:20]
    context_object_name = 'article'

class PostsDetailView(DetailView):
    model = Post
    template_name = 'article_detail.html'
    context_object_name = 'article'

def news_search(request):
    if request.method == 'GET':
        title = request.GET.get('title')
        author = request.GET.get('author')
        publish_date = request.GET.get('created_at')

        filtered_posts = Post.objects.all()

        if title:
            filtered_posts = filtered_posts.filter(title__icontains=title)
        if author:
            filtered_posts = filtered_posts.filter(author__icontains=author)
        if publish_date:
            filtered_posts = filtered_posts.filter(created_at__gte=publish_date)

        context = {
            'posts': filtered_posts,
        }

        return render(request, 'news_search.html', context)
