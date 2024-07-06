from urllib import request

from django.apps import AppConfig
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from datetime import timedelta
from django.utils import timezone
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string




class NewsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'news'

    def ready(self):
        import news.signals

        from apscheduler.schedulers.background import BackgroundScheduler
        import schedule
        import time

        from django.urls import reverse
        from django.contrib.auth import get_user_model
        from news.models import Post, Category
        from django.contrib.auth.models import User

        #User = get_user_model() # ПОКА НЕ НУЖЕН, МОЖЕТ НЕ ПОНАДОБИТЬСЯ


        scheduler = BackgroundScheduler()

        def send_weekly_article_list():
            end_date = timezone.now().date()
            start_date = end_date - timedelta(days=7)

            categories = Category.objects.filter(post_type__in=['article', 'news'])
            subscribers = User.objects.filter(subscribed_categories__in=categories)

            for subscriber in subscribers:
                user_email = subscriber.email

                new_posts = Post.objects.filter(created_at__range=[start_date, end_date],
                                                post_categories__in=categories)

                email_subject = "Weekly Article/News List"
                email_body = "List of new articles/news published this week:\n"

                # for post in new_posts:
                #     post_type = 'articles' if post.post_type == 'article' else 'news'
                #     current_site = get_current_site(request)
                #     post_url = f'http://{current_site}{reverse("post_detail", args=[post_type, post.id])}'
                #     email_body += f"{post.title}: {post.content[:50]} - {get_current_site(None)}{post_url}\n"

                for post in new_posts:
                    post_type = 'articles' if post.post_type == 'article' else 'news'
                    #current_site = get_current_site(request)
                    post_url = f'http://127.0.0.1:8000/login/protect/{post.id}'
                    email_body += f"{post_type} {post.title}: {post.content[:50]} - {get_current_site(None)}{post_url}\n"

                    post.created_at = timezone.make_aware(post.created_at)

                subject = 'Weekly Article/News List'
                message = render_to_string('weekly_email_template.html', {
                    'email_body': email_body,
                })

                email = EmailMultiAlternatives(subject, email_body, 'gefest-173@yandex.ru', [user_email])
                email.attach_alternative(message, 'text/html')
                email.send()

        scheduler.add_job(send_weekly_article_list, 'cron', day_of_week='mon', hour=8)
        scheduler.start()

        # schedule.every(30).seconds.do(send_weekly_article_list)
        #
        # while True:
        #     schedule.run_pending()
        #     time.sleep(1)
