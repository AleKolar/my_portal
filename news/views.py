
from .filters import PostFilter
from .forms import PostForm
from .models import Post
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy


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


def articles_full_detail(request, id):
    post = Post.objects.get(pk=id)
    post_info = {
        'title': post.title,
        'content': post.content,
        'publish_date': post.created_at.strftime('%d.%m.%Y'),
        'author': post.authorname,
    }
    return render(request, 'articles_full_detail.html', {'post': post_info})


class NewsListView(ListView):
    model = Post
    template_name = 'news_list.html'
    queryset = Post.objects.filter(post_type='news').order_by('-created_at')
    context_object_name = 'posts'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        return context


class ArticlesListView(ListView):
    model = Post
    template_name = 'articles_list.html'
    queryset = Post.objects.filter(post_type='article').order_by('-created_at')
    context_object_name = 'posts'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        return context


# def news_search(request): # МНЕ ЭТО КАЖЕТСЯ ОЧ. ПРЯМОЛИНЕЙНЫМ ПОДХОДОМ и классным, хотя filtrs то же хорош и не с проста на него ставят
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


class PostsListView(ListView):
    model = Post
    ordering = 'authorname', 'created_at'
    template_name = 'news_search.html'
    # queryset = Post.objects.filter(post_type='article').order_by('-created_at')[:20]
    ###queryset = Post.objects.all().order_by('-created_at')
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        # return self.filterset.qs
        if self.filterset.is_bound and self.filterset.is_valid():
            queryset = self.filterset.qs
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        return context


class PostCreate(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'create.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        if self.request.path == '/news/create/':
            form.instance.post_type = 'news'
            return super().form_valid(form)
        else:
            form.instance.post_type = 'article'
            return super().form_valid(form)


class PostUpdate(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'edit.html'


class PostDelete(DeleteView):
    model = Post
    #form_class = PostForm
    template_name = 'delete.html'

    def get_success_url(self):
        post_type = self.object.post_type
        if post_type == 'news':
            return reverse_lazy('news_list')
        elif post_type == 'article':
            return reverse_lazy('articles_list')





