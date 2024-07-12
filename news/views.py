from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .filters import PostFilter
from .forms import PostForm
from .models import Post, Author, Category, PostCategory
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import HttpResponse, Http404, JsonResponse
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.views.generic import View
from .tasks import save_post_and_notify



User = get_user_model()


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
    news_article = get_object_or_404(Post, id=id)
    return render(request, 'news_full_detail.html', {'post': news_article, 'id': id})


@login_required
def articles_full_detail(request, id):
    post = Post.objects.get(pk=id)
    post_info = {
        'title': post.title,
        'content': post.content,
        'publish_date': post.created_at.strftime('%d.%m.%Y'),
        'author': post.authorname,
    }
    news_article = get_object_or_404(Post, id=id)
    return render(request, 'articles_full_detail.html', {'post': news_article, 'id': id})


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

class SubscribeToNewsView(View):
    @method_decorator(csrf_exempt)
    def post(self, request, *args, **kwargs):
        news_category, _ = Category.objects.get_or_create(name='Category 1', post_type='news')
        news_category.subscribers.add(request.user)
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

class SubscribeToArticlesView(View):
    @method_decorator(csrf_exempt)
    def post(self, request, *args, **kwargs):
        articles_category, _ = Category.objects.get_or_create(name='Category 2', post_type='article')
        articles_category.subscribers.add(request.user)
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


class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'create.html'
    def dispatch(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='authors').exists():
            messages.error(request, 'You need to be an author to create news and articles.')
            return redirect('/')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        post = form.save(commit=False)
        author, created = Author.objects.get_or_create(user=self.request.user)
        post.author_id = author.id###
        ###post.author = author
        #post.author = self.request.user.author
        post_type = 'news' if self.request.path == '/news/create/' else 'article'
        form.instance.post_type = post_type

        post_type = 'news' if self.request.path == '/news/create/' else 'article'
        form.instance.post_type = post_type

        if post_type == 'news':
            category_name = 'News'
            post_category = 'Category 1'
        else:
            category_name = 'Articles'
            post_category = 'Category 2'

        category, _ = Category.objects.get_or_create(name=category_name, post_type=post_type)
        post.category = category
        post.save()

        category, _ = Category.objects.get_or_create(name=post_category)
        PostCategory.objects.create(post=post, category=category)

        # 2, 3  form_valid , чтоб вызывала эту "сохранения поста и отправки уведомлений( save_post_and_notify )" задачу вместо сохранения поста напрямую
        post_data = form.cleaned_data
        save_post_and_notify.delay(post_data)
        return super(PostCreate, self).form_valid(form)



class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'edit.html'


class PostDelete(LoginRequiredMixin, DeleteView):
    model = Post
    # form_class = PostForm
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





# import logging
#
# logger = logging.getLogger(__name__)
#
# class CustomCategoryError(Exception):
#     pass
#
#
# def your_view_method(get_instance_somehow):
#     instance = get_instance_somehow()
#
#     subscribed_users = []  # Initialize subscribed_users as empty list
#
#     first_category = instance.categories.first()
#     if first_category is not None:
#         subscribed_users = first_category.subscribers.all()
#     else:
#         pass


def subscribe_news(request):
    try:
        news_category = Category.objects.get(name='News', post_type='news')
    except ObjectDoesNotExist:
        news_category = Category.objects.create(name='News', post_type='news')

    news_category.subscribe_user(request.user)
    return JsonResponse({'message': 'Subscribed to News successfully'}, status=200)

def subscribe_articles(request):
    try:
        articles_category = Category.objects.get(name='Articles', post_type='article')
    except ObjectDoesNotExist:
        articles_category = Category.objects.create(name='Articles', post_type='article')

    articles_category.subscribe_user(request.user)
    return JsonResponse({'message': 'Subscribed to Articles successfully'}, status=200)