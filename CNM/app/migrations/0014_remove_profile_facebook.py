# Generated by Django 5.0.4 on 2024-05-10 05:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_posts_video'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='facebook',
        ),
    ]
