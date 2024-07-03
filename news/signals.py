from allauth.account.utils import user_email
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.core.signals import request_finished
from news.models import Post, Subscription
from django.utils import timezone


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