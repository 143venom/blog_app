# Generated by Django 4.2.7 on 2023-12-09 13:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog_app', '0003_friendship_created_at'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Friendship',
        ),
    ]