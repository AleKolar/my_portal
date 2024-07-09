from sched import scheduler
from urllib import request
from django.apps import AppConfig
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from datetime import timedelta
from django.utils import timezone
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from news.models import Post, Category




class NewsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'news'

    def ready(self):
        import news.signals

        # from apscheduler.schedulers.background import BackgroundScheduler
        # import schedule
        # import time
        #
        # from django.urls import reverse
        # from django.contrib.auth import get_user_model
        # from news.models import Post, Category
        # from django.contrib.auth.models import User
        #
        # #User = get_user_model() # ПОКА НЕ НУЖЕН, МОЖЕТ НЕ ПОНАДОБИТЬСЯ
        #
        #
        # scheduler = BackgroundScheduler()
        #
        # def send_weekly_article_list():
        #     end_date = timezone.now().date()
        #     start_date = end_date - timedelta(days=7)
        #
        #     categories = Category.objects.filter(post_type__in=['article', 'news'])
        #     subscribers = User.objects.filter(subscribed_categories__in=categories)
        #
        #     for subscriber in subscribers:
        #         user_email = subscriber.email
        #
        #         list_of_posts = []
        #
        #         #new_posts = Post.objects.all() # ТЕСТИЛ
        #         new_posts = Post.objects.filter(created_at__range=[start_date, end_date],
        #                                         post_categories__in=categories)
        #
        #         email_subject = "Weekly Article/News List"
        #         email_body = f"List of new articles/news published this week:\n"
        #
        #         for post in new_posts:
        #             post_type = 'article' if post.post_type == 'article' else 'news'
        #             post_url = f'http://127.0.0.1:8000/login/protect/{post.id}'
        #             post_link = f'<a href="{post_url}">{post.title}</a>'
        #             email_body += f"{post_type}: {post_link} - {post.content[:50]}\n"
        #             list_of_posts.append({'title': post.title, 'content': post.content[:50], 'post_url': post_url})
        #
        #         subject = 'Weekly Article/News List'
        #         html_message = render_to_string('weekly_email_template.html', {
        #             'email_body': email_body,
        #             'new_posts': list_of_posts,
        #         })
        #         plain_message = "This is the plain text version of the email."
        #
        #         send_mail(
        #             subject,
        #             plain_message,
        #             'gefest-173@yandex.ru',
        #             [user_email],
        #             html_message=html_message,
        #         )
        #
        # scheduler.add_job(send_weekly_article_list, 'cron', day_of_week='mon', hour=8)
        # scheduler.start()
        #
        # Тестил, опасная вещь к базе данных нельзя, то нельзя , не успел импортироваться
        # schedule.every(30).seconds.do(send_weekly_article_list)
        #
        # while True:
        #     schedule.run_pending()
        #     time.sleep(1)


