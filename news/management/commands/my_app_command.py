from django.core.management.base import BaseCommand, CommandError
from news.models import Post
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Deletes all news posts from two weeks ago with user consent'

    def handle(self, *args, **options):
        two_weeks_ago = datetime.now() - timedelta(weeks=2)
        news_to_delete = Post.objects.filter(post_type='news', created_at__lte=two_weeks_ago)

        if news_to_delete.exists():
            self.stdout.write('Do you really want to delete content? yes/no')
            answer = input().strip()

            if answer == 'yes':
                news_to_delete.delete()
                self.stdout.write(self.style.SUCCESS('Successfully deleted news posts from two weeks ago!'))
            else:
                self.stdout.write(self.style.ERROR('Deletion cancelled by user'))
        else:
            self.stdout.write(self.style.ERROR('No news posts from two weeks ago found'))
