# Generated by Django 4.2.6 on 2023-10-27 03:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_posts', '0005_alter_apppost_categories_alter_apppost_content_and_more'),
        ('authors', '0004_alter_author_followers'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='my_posts',
            field=models.ManyToManyField(blank=True, related_name='posts_i_see', to='app_posts.apppost'),
        ),
    ]
