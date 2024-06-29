from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.dispatch import Signal
from django.http import request
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.utils.html import strip_tags
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from .filters import PostFilter
from .forms import PostForm
from .models import Post, Category, Author
from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy


def index(request):
    return render(request, 'index.html')

@login_required
def news_full_detail(request, id):
    post = Post.objects.get(pk=id)
    post_info = {
        'title': post.title,
        'content': post.content,
        'publish_date': post.created_at.strftime('%d.%m.%Y'),
        'author': post.authorname,

    }
    return render(request, 'news_full_detail.html', {'post': post_info})

@login_required
def articles_full_detail(request, id):
    post = Post.objects.get(pk=id)
    post_info = {
        'title': post.title,
        'content': post.content,
        'publish_date': post.created_at.strftime('%d.%m.%Y'),
        'author': post.authorname,
    }
    return render(request, 'articles_full_detail.html', {'post': post_info})

@method_decorator(login_required, name='dispatch')
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

    @method_decorator(csrf_exempt)
    def post(self, request, *args, **kwargs):
        articles_posts = Post.objects.filter(post_type='news')
        for post in articles_posts:
            post.subscribers.add(request.user)
        return redirect('news_list')


class ArticlesListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'articles_list.html'
    queryset = Post.objects.filter(post_type='article').order_by('-created_at')
    context_object_name = 'posts'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        return context

    @method_decorator(csrf_exempt)
    def post(self, request, *args, **kwargs):
        articles_posts = Post.objects.filter(post_type='article')
        for post in articles_posts:
            post.subscribers.add(request.user)
        return redirect('articles_list')


class PostsListView(LoginRequiredMixin, ListView):
    model = Post
    ordering = 'authorname', 'created_at'
    template_name = 'news_search.html'
    context_object_name = 'posts'
    paginate_by = 10


    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context

addpost = Signal()
class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'create.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        author, created = Author.objects.get_or_create(user=self.request.user)
        post.author = author
        post_type = 'news' if self.request.path == '/news/create/' else 'article'
        form.instance.post_type = post_type
        post.save()
        subscribed_users = post.author.subscribers.all()

        for user in subscribed_users:
            subject = 'New {} Released!'.format(post_type.capitalize())
            html_message = render_to_string('email_template.html', {'post': post, 'post_type': post_type})
            plain_message = strip_tags(html_message)
            from_email = 'gefest-173@yandex.ru'
            to_email = user.email
            send_mail(subject, plain_message, from_email, [to_email], html_message=html_message)

        return super().form_valid(form)


class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'edit.html'


class PostDelete(LoginRequiredMixin, DeleteView):
    model = Post
    #form_class = PostForm
    template_name = 'delete.html'

    def get_success_url(self):
        post_type = self.object.post_type
        if post_type == 'news':
            return reverse_lazy('news_list')
        elif post_type == 'article':
            return reverse_lazy('articles_list')


# ПОКА НЕ НАДО , ПОПРОБУЕМ , НЕМНОГО ПО ДРУГОМУ
# # SO add users for newsletters from me (while adding news)
# class SubscribeToCategory(View):
#     def post(self, request, *args, **kwargs):
#         category_name = request.POST.get('post_type')
#         user = request.user
#
#         if category_name == 'news':
#             category = Category.objects.get(name='news')
#             category.subscribers.add(user)
#             return redirect('news_list')
#         elif category_name == 'articles':
#             category = Category.objects.get(name='articles')
#             category.subscribers.add(user)
#             return redirect('articles_list')
#         else:
#             return redirect('news_list')