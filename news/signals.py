from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User, Group
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives, send_mail
from .views import addpost

from .models import Post

# Электронное письмо отправляется при создании нового сообщения
# Электронное письмо не отправляется, если сообщение обновлено, а не создано

@receiver(post_save, sender=Post)
def send_email_on_new_post(sender, instance, created, **kwargs):
    if created:
        subject = instance.title
        message = instance.content[:50]
        html_message = render_to_string('email_template.html', {'title': instance.title, 'content': instance.content[:50]})
        send_mail(subject, message, 'gefest-173@yandex.ru', [instance.author.user.email], html_message=html_message)