
from datetime import timedelta, datetime
from celery import shared_task
from celery.utils.log import get_task_logger
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone
from django.core.exceptions import ValidationError
from news.models import Category, Post, Author
import logging



#logger = logging.getLogger(__name__)


@shared_task
def send_email_notification_to_subscribers(post_name, post_content, created, post_id):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        print(f"Post with id {post_id} does not exist")
        return

    post_type = post.post_type

    if created and post_type in ['news', 'article']:
        category = post.category
        subscribers = User.objects.filter(subscribed_categories=category)

        for subscriber in subscribers:
            user_email = subscriber.email
            username = subscriber.username
            post_title = post.title
            post_url = f'http://127.0.0.1:8000/login/protect/{post.id}'
            html_message = f"<h2>Hello, {username}! New {post_type}: {post_title}</h2><p>{post_content[:50]}</p><a href='{post_url}'>Read more</a>"
            plain_message = f"Hello, {username}. A new {post_type} is available: {post_title}\n\n{post_content[:50]}\nRead more at: {post_url}"

            # logger.debug("Starting email notification task...")

            try:
                send_mail(
                    post_title,
                    plain_message,
                    'gefest-173@yandex.ru',
                    [user_email],
                    html_message=html_message,
                )
                print(f"Email sent to {user_email}")
                # logger.info(f"Email sent to {user_email}")
            except Exception as e:
                print(f"Failed to send email to {user_email}: {str(e)}")
                # logger.error(f"Failed to send email to {user_email}: {str(e)}")



start_date = datetime.now() - timedelta(days=7)
end_date = datetime.now()

@shared_task
def send_weekly_article_list():
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
