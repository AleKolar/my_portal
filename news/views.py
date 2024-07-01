from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import Signal, receiver
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from .filters import PostFilter
from .forms import PostForm
from .models import Post, Category, Author, Subscription
from django.shortcuts import render, redirect, get_object_or_404
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
    news_article = get_object_or_404(Post, id=id)
    return render(request, 'news_full_detail.html', {'post': news_article})

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
    return render(request, 'articles_full_detail.html', {'post': news_article})

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

#addpost = Signal()

@receiver(post_save, sender=Post)
def send_email_on_new_post(sender, instance, created, **kwargs):
    if created:
        subject = instance.title
        message = instance.content[:50]
        html_message = render_to_string('email_template.html',
                                        {'title': instance.title, 'content': instance.content[:50],
                                         'post_url': instance.get_absolute_url(), 'post_id': instance.id})

        post_type = 'news' if instance.post_type == 'news' else 'article'
        subscribers = Subscription.objects.filter(
            news_subscription=True) if post_type == 'news' else Subscription.objects.filter(article_subscription=True)

        if subscribers.exists():
            for subscriber in subscribers:
                send_mail(subject, message, 'gefest-173@yandex.ru', [subscriber.user.email], html_message=html_message)


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

        if created:
            send_email_on_new_post(Post, post, created)

        return super(PostCreate, self).form_valid(form)

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


def subscribe_articles(request):
    if request.method == 'POST':
        Subscription.objects.create(user=request.user, articles_subscription=True)
        return redirect('articles_list')

def subscribe_news(request):
    if request.method == 'POST':
        Subscription.objects.create(user=request.user, news_subscription=True)
        return redirect('news_list')
