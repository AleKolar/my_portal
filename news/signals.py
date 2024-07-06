from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Post


published_news_count = {}

@receiver(post_save, sender=Post)
def send_email_notification_to_subscribers(sender, instance, created, **kwargs):
    if created and instance.post_type in ['news', 'article']:
        user = instance.author.user
        current_date = timezone.now().date()

        if user in published_news_count:
            if published_news_count[user]['date'] == current_date and published_news_count[user]['count'] >= 3:
                raise ValidationError("You have reached the daily limit for publishing news items.")
            elif published_news_count[user]['date'] != current_date:
                published_news_count[user] = {'date': current_date, 'count': 1}
            else:
                published_news_count[user]['count'] += 1
        else:
            published_news_count[user] = {'date': current_date, 'count': 1}

        subscribers = instance.category.subscribers.all()
        post_url = f'http://ALLOWED_HOSTS/{instance.post_type}/{instance.id}'

        print(f"Number of Subscribers: {subscribers.count()}")

        # ТУТ ДОСТАЮ ДАННЫЕ ИЗ table user
        for subscriber in subscribers:
            id = subscriber.id
            user = User.objects.get(pk=id)
            username = user.username
            user_email = user.email
            post_title = instance.title
            post_content = instance.content
            print(f'EMAIL: {user_email}, {instance.post_type}')

            post_url = f'http://127.0.0.1:8000/login/protect/{instance.id}'
            html_message = f"<h2>Здравствуй,{subscriber.username} Новая статья {post_title} в твоём любимом разделе {instance.post_type}!</h2><p>{post_content[:50]}</p><a href='{post_url}'>Read more</a>"
            plain_message = f"Hello, {subscriber.username}. A new {instance.post_type} in your favorite section!\n\n{post_title}: {post_content[:50]}\nRead more at: {post_url}"

            print(f"Sending email to: {user_email}, {subscriber.username}")  # Debug statement

            send_mail(
                post_title,
                plain_message,
                'gefest-173@yandex.ru',
                [user_email],
                html_message=html_message,
            )

# НЕ ЗАБЫТЬ! НЕ БОЛЕЕ ТРЕХ В ДЕНЬ
#             user = instance.author
#             today = datetime.now().date()
#             posts_today = Post.objects.filter(author=user, created_at__date=today).count()
#
#             if posts_today <= 2:
#                 subscribed_users = instance.categories.first().subscribers.all()
#
#                 for user in subscribed_users:
#
#             else:
#                 raise "превышен дневной лимит"

