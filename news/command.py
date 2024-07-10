# from django.core.management.base import BaseCommand
# from django.utils import timezone
# from datetime import timedelta
# from news.models import Post, Category
# from django.contrib.auth.models import User
# from django.core.mail import send_mail
# from django.template.loader import render_to_string
# from apscheduler.schedulers.background import BackgroundScheduler
# from apscheduler.triggers.cron import CronTrigger
# from django_apscheduler.jobstores import DjangoJobStore
# import logging
# from django.conf import settings
#
# ### ИСПОЛШЬЗУЕМ COMMAND
#
# logger = logging.getLogger(__name__)
#
#
# class Command(BaseCommand):
#     help = "Runs apscheduler."
#
#     @staticmethod
#     def my_job(self):
#         start_date = timezone.now().date() - timedelta(days=7)
#         end_date = timezone.now().date()
#         categories = Category.objects.filter(post_type__in=['article', 'news'])
#         subscribers = User.objects.filter(subscribed_categories__in=categories)
#
#         for subscriber in subscribers:
#             user_email = subscriber.email
#             list_of_posts = []
#             new_posts = Post.objects.filter(created_at__range=[start_date, end_date],
#                                             post_categories__in=categories)
#             email_subject = "Weekly Article/News List"
#             email_body = f"List of new articles/news published this week:\n"
#
#             for post in new_posts:
#                 post_type = 'article' if post.post_type == 'article' else 'news'
#                 post_url = f'http://127.0.0.1:8000/login/protect/{post.id}'
#                 post_link = f'<a href="{post_url}">{post.title}</a>'
#                 email_body += f"{post_type}: {post_link} - {post.content[:50]}\n"
#                 list_of_posts.append({'title': post.title, 'content': post.content[:50], 'post_url': post_url})
#
#             subject = 'Weekly Article/News List'
#             html_message = render_to_string('weekly_email_template.html', {
#                 'email_body': email_body,
#                 'new_posts': list_of_posts,
#             })
#             plain_message = "This is the plain text version of the email."
#
#             send_mail(
#                 subject,
#                 plain_message,
#                 'gefest-173@yandex.ru',
#                 [user_email],
#                 html_message=html_message,
#             )
#
#     def handle(self, *args, **options):
#         scheduler = BackgroundScheduler(timezone=settings.TIME_ZONE)
#         scheduler.add_jobstore(DjangoJobStore(), "default")
#
#         scheduler.add_job(
#             self.my_job,
#             trigger=CronTrigger(day_of_week='mon', hour=8),
#             id='send_weekly_article_list',
#             replace_existing=True,
#         )
#
#         try:
#             logger.info("Starting scheduler...")
#             scheduler.start()
#         except KeyboardInterrupt:
#             logger.info("Stopping scheduler...")
#             scheduler.shutdown()
#             logger.info("Scheduler shut down successfully!")
