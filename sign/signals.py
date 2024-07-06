from allauth.account.signals import user_signed_up
from django.core.mail import send_mail, EmailMultiAlternatives
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


from allauth.account.utils import user_email, user_field


@receiver(user_signed_up)
def send_welcome_email(request, user, **kwargs):
    activate_url = user_email(user)
    subject = 'Welcome'
    message = render_to_string('custom_confirm_email.html', {
        'user': user,
        'activate_url': activate_url
    })

    email = EmailMultiAlternatives(subject, message, 'gefest-173@yandex.ru', [user.email])
    email.attach_alternative(message, 'text/html')
    email.send()

