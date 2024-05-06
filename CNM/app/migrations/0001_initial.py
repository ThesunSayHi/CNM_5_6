# Generated by Django 5.0.4 on 2024-05-05 07:54

import app.models
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('username', models.CharField(error_messages={'unique': 'The username already exists.'}, help_text='30 characters or less required. Contains only letters, numbers, and characters @/./+/-/_', max_length=30, unique=True, verbose_name='username')),
                ('is_superuser', models.BooleanField(default=False, help_text='Specify the user who has all system administrative rights.', verbose_name='superuser status')),
                ('is_staff', models.BooleanField(default=False, help_text='Specify users with access to the admin page.', verbose_name='staff status')),
                ('is_posters', models.BooleanField(default=False, help_text='Specify users with permission to post', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Specify the user who is considered "active". Unselect to deactivate this account.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now)),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='LastLogin')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'User',
                'ordering': ['username'],
            },
        ),
        migrations.CreateModel(
            name='Posts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, null=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('address', models.CharField(blank=True, max_length=255, null=True)),
                ('available', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
                ('posted_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]