# Generated by Django 5.0.4 on 2024-06-16 17:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='authorname',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
