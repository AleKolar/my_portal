from django.db.models import Q

from .filters import PostFilter
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
        'author': post.authorname,
    }
    return render(request, 'news_full_detail.html', {'post': post_info})

class NewsListView(ListView):
    model = Post
    template_name = 'news_list.html'
    #ordering = ['title', 'author', '-created_at'] # разбираюсь с постраничным выводом
    #queryset = Post.objects.filter(post_type='news').order_by('-created_at')
    queryset = Post.objects.all().order_by('-created_at') # разбираюсь с постраничным выводом
    context_object_name = 'posts' # разбираюсь с постраничным выводом
    paginate_by = 10# разбираюсь с постраничным выводом

class NewsDetailView(DetailView):
    model = Post
    template_name = 'news_full_detail.html'
    context_object_name = 'news'





# def news_search(request):
#     if request.method == 'GET':
#         title = request.GET.get('title')
#         author = request.GET.get('authorname')
#         publish_date = request.GET.get('created_at')
#
#         filtered_posts = Post.objects.all()
#
#         if title:
#             filtered_posts = filtered_posts.filter(title__icontains=title)
#         if author:
#             filtered_posts = filtered_posts.filter(author__icontains=author)
#         if publish_date:
#             filtered_posts = filtered_posts.filter(created_at__gte=publish_date)
#
#         context = {
#             'posts': filtered_posts,
#         }
#
#         return render(request, 'news_search.html', context)


# def news_search(request):
#     q = request.GET.get('q') if request.GET.get('q') != None else ''
#     filtered_posts = Post.objects.filter(
#         Q(title__contains=q) |
#         Q(authorname__contains=q) |
#         Q(created_at__icontains=q)
#     )
#     posts = Post.objects.all()
#     context = {'filtered_posts': filtered_posts, 'posts': posts}
#     return render(request, 'news_search.html', context)

class PostsListView(ListView):
    model = Post
    ordering = 'authorname', 'created_at'
    template_name = 'news_search.html'
    #queryset = Post.objects.filter(post_type='article').order_by('-created_at')[:20]
    ###queryset = Post.objects.all().order_by('-created_at')
    context_object_name = 'posts'
    paginate_by = 2
    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # self.request.GET содержит объект QueryDict, который мы рассматривали
        # в этом юните ранее.
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = PostFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список товаров
        #return self.filterset.qs
        if self.filterset.is_bound and self.filterset.is_valid():
            queryset = self.filterset.qs
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        return context


class ProductDetail(DetailView):
    model = Post
    template_name = 'news_search.html'
    context_object_name = 'posts'