from allauth.account.utils import user_email
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.core.signals import request_finished
from news.models import Post, Subscription


# Электронное письмо отправляется при создании нового сообщения
# Электронное письмо не отправляется, если сообщение обновлено, а не создано

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
            news_subscription=True) if post_type == 'news' else Subscription.objects.filter(articles_subscription=True)

        if subscribers.exists():
            for subscriber in subscribers:
                try:
                    user_email = subscriber.user.email
                    send_mail(subject, message, 'gefest-173@yandex.ru', [user_email], html_message=html_message)
                except ObjectDoesNotExist:
                    print(f'User does not exist for subscriber: {subscriber.id}')
        else:
            print('No subscribers found')

@receiver(request_finished)
def send_email_on_request_finished(sender, **kwargs):
    subject = 'Request Processed Successfully'
    message = 'Thank you for visiting.'
    recipient_email = [user_email]

    send_mail(subject, message, 'gefest-173@yandex.ru', recipient_email)