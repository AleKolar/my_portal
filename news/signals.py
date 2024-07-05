from django.core.exceptions import ObjectDoesNotExist
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.urls import reverse

from .models import Post
from datetime import datetime, timedelta



@receiver(post_save, sender=Post)
def send_email_notification_to_subscribers(sender, instance, created, **kwargs):
    if created and instance.post_type in ['news', 'article']:
        subscribers = instance.category.subscribers.all()
        post_url = f'http://ALLOWED_HOSTS/{instance.post_type}/{instance.id}'

        for subscriber in subscribers:
            user_email = subscriber.email
            post_title = instance.title
            post_content = instance.content

            html_message = f"<h2>{post_title}</h2><p>{post_content[:50]}</p><a href='{post_url}'>Read more</a>"
            plain_message = f"Hello, {subscriber.username}. A new {instance.post_type} in your favorite section!\n\n{post_title}: {post_content[:50]}\nRead more at: {post_url}"

            send_mail(
                post_title,
                plain_message,
                'gefest-173@yandex.ru',
                [user_email],
                html_message=html_message,
            )
# @receiver(post_save, sender=Post)
# def send_email_on_new_post(sender, instance, created, **kwargs):
#     if created:
#         if instance.categories.first():
#             subscribed_users = instance.categories.first().subscribers.all()
#
#             user = instance.author
#             today = datetime.now().date()
#             posts_today = Post.objects.filter(author=user, created_at__date=today).count()
#
#             if posts_today <= 2:
#                 subscribed_users = instance.categories.first().subscribers.all()
#
#                 for user in subscribed_users:
#                     if user.email:
#                         subject = 'New Post Notification'
#
#                         if instance.post_type == 'news':
#                             template = 'news_full_detail.html'
#                         else:
#                             template = 'articles_full_detail.html'
#
#                         email_content = render_to_string(template, {'post': instance})
#                         message = f'New post: {instance.title[:50]}\n\nRead more: {reverse("post_detail", args=[instance.id])}'
#
#                         send_mail(subject, message, 'gefest-173@yandex.ru', [user.email], html_message=email_content)
#             else:
#                 raise "превышен дневной лимит"



#
# @receiver(addpost)
# def send_email_on_new_post(sender, instance, created, **kwargs):
#     if created:
#         subject = instance.title
#         message = instance.content[:50]
#         html_message = render_to_string('email_template.html',
#                                         {'title': instance.title, 'content': instance.content[:50],
#                                          'post_url': instance.get_absolute_url(), 'post_id': instance.id})
#
#         if instance.post_type == 'news':
#             user = instance.author.user
#             today = timezone.now()
#             start_of_day = today.replace(hour=0, minute=0, second=0, microsecond=0)
#             end_of_day = today.replace(hour=23, minute=59, second=59, microsecond=999999)
#
#             news_count = Post.objects.filter(author__user=user, post_type='news', created_at__range=(start_of_day, end_of_day)).count()
#
#             if news_count >= 3:
#                 print('limit 3 posts')
#                 return
#
#         subscribers = Subscription.objects.filter(news_subscription=True) if instance.post_type == 'news' else Subscription.objects.filter(articles_subscription=True)
#
#         if subscribers.exists():
#             for subscriber in subscribers:
#                 try:
#                     user_email = subscriber.user.email
#                     send_mail(subject, message, 'gefest-173@yandex.ru', [user_email], html_message=html_message)
#                 except ObjectDoesNotExist:
#                     print(f'User does not exist for subscriber: {subscriber.id}')
#         else:
#             print('No subscribers found')

# @receiver(request_finished)
# def send_email_on_request_finished(sender, **kwargs):
#     subject = 'Request Processed Successfully'
#     message = 'Thank you for REGISTRATION'
#     recipient_email = [user_email]
#
#     send_mail(subject, message, 'gefest-173@yandex.ru', recipient_email)