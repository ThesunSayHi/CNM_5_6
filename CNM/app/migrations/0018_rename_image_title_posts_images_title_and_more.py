# Generated by Django 5.0.4 on 2024-05-10 11:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0017_rename_image_posts_image_title_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='posts',
            old_name='image_title',
            new_name='images_title',
        ),
        migrations.RemoveField(
            model_name='posts',
            name='images',
        ),
    ]