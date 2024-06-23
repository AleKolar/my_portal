
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Author, Profile

@receiver(post_save, sender=Author)
def create_author_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(author=instance)

@receiver(post_save, sender=Author)
def save_author_profile(sender, instance, **kwargs):
    instance.profile.save()

