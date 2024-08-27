from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .filters import PostFilter
from .forms import PostForm, CommentForm
from .models import Post, Author, Category, PostCategory
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import HttpResponse, Http404, JsonResponse
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.views.generic import View
from .tasks import send_email_notification_to_subscribers
from django.forms.models import model_to_dict
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from django.utils.translation import gettext as _

User = get_user_model()


class Index(View):
    def get(self, request):
        string = _('Hello world')
        context = {'string': string}
        return HttpResponse(render(request, 'index_msg.html', context))

def index(request):
    return render(request, 'index.html')


#@cache_page(300)
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


# @cache_page(300)
@login_required
def articles_full_detail(request, id):
    post = get_object_or_404(Post, id=id)
    post_info = {
        'title': post.title,
        'content': post.content,
        'publish_date': post.created_at.strftime('%d.%m.%Y'),
        'author': post.authorname,
    }

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.post = post
            new_comment.user = request.user
            author_instance = Author.objects.get(user=request.user)
            new_comment.author = author_instance
            new_comment.save()
            messages.success(request, "Comment added successfully!")
    else:
        form = CommentForm()

    return render(request, 'articles_full_detail.html', {'post': post, 'id': id, 'comment_form': form}, )


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
        if not self.request.user.groups.filter(name='authors').exists():
            messages.error(self.request, 'You need to be an author to create news and articles.')
            return redirect('/')

        author, created = Author.objects.get_or_create(user=self.request.user)
        post = form.save(commit=False)
        post.author = author

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

        post_data = model_to_dict(post)
        post_name = post_data.get('title')
        post_content = post_data.get('content')[:50]

        created = True
        send_email_notification_to_subscribers.delay(post_name, post_content, created, post.id)
        return super().form_valid(form)


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


def q_news(request):
    posts = Post.objects.all()
    return render(request, 'q_news.html', {'posts': posts})
