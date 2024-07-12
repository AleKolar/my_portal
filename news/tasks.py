import json
from datetime import timedelta
from celery import shared_task
from celery.utils.log import get_task_logger
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone
from django.core.exceptions import ValidationError
from news.models import Category, Post, Author
import logging

logger = logging.getLogger('news')


@shared_task
def save_post_and_notify(post_data):
    author_data = post_data.get('author')  # Retrieve the 'author' data from post_data if it exists
    if author_data:
        author, created = Author.objects.get_or_create(user=author_data)
        post_data['author_id'] = author.id

        logger.info("Received post_data in save_post_and_notify: %s", post_data)
        logger.debug('Test message')

        # Ensure 'author_id' is included in the post_data
        post = Post.objects.create(author_id=post_data['author_id'], **post_data)
        send_email_notification_to_subscribers.delay(post.id, True)
    else:
        logger.error("Author data is missing in post_data")


# 1. Надо - создать отдельную задачу Celery для сохранения поста и отправки уведомленийб , чтобы она использовала Celery задачу
@shared_task
def send_email_notification_to_subscribers(post_id, created):
    post = Post.objects.get(id=post_id)
    published_news_count = {}
    current_date = timezone.now().date()

    if created and post.post_type in ['news', 'article']:
        user = post.author.user

        if user in published_news_count:
            if published_news_count[user]['date'] == current_date and published_news_count[user]['count'] >= 3:
                raise ValidationError("You have reached the daily limit for publishing news items.")
            elif published_news_count[user]['date'] != current_date:
                published_news_count[user] = {'date': current_date, 'count': 1}
            else:
                published_news_count[user]['count'] += 1
        else:
            published_news_count[user] = {'date': current_date, 'count': 1}

            subscribers = post.category.subscribers.all()

        for subscriber in subscribers:
            user = User.objects.get(pk=subscriber.id)
            username = user.username
            user_email = user.email
            post_title = post.title
            post_content = post.content

            post_url = f'http://127.0.0.1:8000/login/protect/{post.id}'
            html_message = f"<h2>Здравствуй, {username} Новая статья {post_title} в твоём любимом разделе {post.post_type}!</h2><p>{post_content[:50]}</p><a href='{post_url}'>Read more</a>"
            plain_message = f"Hello, {username}. A new {post.post_type} in your favorite section!\n\n{post_title}: {post_content[:50]}\nRead more at: {post_url}"

            send_mail(
                post_title,
                plain_message,
                'gefest-173@yandex.ru',
                [user_email],
                html_message=html_message,
            )


@shared_task
def send_weekly_article_list():
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=7)

    categories = Category.objects.filter(post_type__in=['article', 'news'])
    subscribers = User.objects.filter(subscribed_categories__in=categories)

    for subscriber in subscribers:
        user_email = subscriber.email

        list_of_posts = []

        new_posts = Post.objects.filter(created_at__range=[start_date, end_date], post_categories__in=categories)

        email_subject = "Weekly Article/News List"
        email_body = f"List of new articles/news published this week:\n"

        for post in new_posts:
            post_type = 'article' if post.post_type == 'article' else 'news'
            post_url = f'http://127.0.0.1:8000/login/protect/{post.id}'
            post_link = f'<a href="{post_url}">{post.title}</a>'
            email_body += f"{post_type}: {post_link} - {post.content[:50]}\n"
            list_of_posts.append({'title': post.title, 'content': post.content[:50], 'post_url': post_url})

        subject = 'Weekly Article/News List'
        html_message = render_to_string('weekly_email_template.html', {
            'email_body': email_body,
            'new_posts': list_of_posts,
        })
        plain_message = "This is the plain text version of the email."

        send_mail(
            subject,
            plain_message,
            'gefest-173@yandex.ru',
            [user_email],
            html_message=html_message,
        )
