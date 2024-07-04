from allauth.account.signals import user_signed_up
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string

from .models import Author, Profile

@receiver(post_save, sender=Author)
def create_author_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(author=instance)

@receiver(post_save, sender=Author)
def save_author_profile(sender, instance, **kwargs):
    instance.profile.save()


@receiver(user_signed_up)
def send_welcome_email(sender, **kwargs):
    user = kwargs['user']
    email = user.email

    subject = 'Welcome to my News Application!'

    # Load your HTML email template
    html_message = render_to_string('custom_confirm_email.html', {'user': user})

    send_mail(subject, None, 'gefest-173@yandex.ru', [email], html_message=html_message)