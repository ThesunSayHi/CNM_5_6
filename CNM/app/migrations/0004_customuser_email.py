# Generated by Django 5.0.4 on 2024-05-07 01:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_posts_description_posts_images1_posts_images2_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='email',
            field=models.EmailField(max_length=254, null=True, unique=True),
        ),
    ]
