# Generated by Django 5.0.4 on 2024-06-18 19:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0002_alter_post_authorname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='authorname',
            field=models.CharField(max_length=255),
        ),
    ]
