import os
from django.core.mail import send_mail


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'my_portal.settings')

send_mail('Subject', 'Message', 'gefest-173@yandex.ru', ['alek.kolark@gmail.com'])